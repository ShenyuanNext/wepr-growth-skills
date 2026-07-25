#!/usr/bin/env bash
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geoflow-cli
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

set -euo pipefail

workspace="${1:-}"
config_path="${2:-}"
preflight_checks="${3:-${GEOFLOW_PREFLIGHT_CHECKS:-catalog}}"

if [[ -z "$workspace" ]]; then
  echo "Usage: geoflow_preflight.sh <workspace> [config]" >&2
  exit 1
fi

if [[ ! -d "$workspace" ]]; then
  echo "Workspace not found: $workspace" >&2
  exit 1
fi

cli_path="$workspace/bin/geoflow"

api_base_url="${GEOFLOW_BASE_URL:-}"
api_token="${GEOFLOW_API_TOKEN:-}"
admin_path="${GEOFLOW_ADMIN_PATH:-/admin}"

docker_hint() {
  if [[ -f "$workspace/docker-compose.yml" || -f "$workspace/compose.yml" ]]; then
    cat >&2 <<'EOF'
Docker Compose workspace detected. For Laravel API fallback:
  1. confirm containers are running: docker compose ps
  2. confirm API routes: docker compose exec app php artisan route:list --path=api/v1
  3. set GEOFLOW_BASE_URL to the exposed web root, e.g. http://127.0.0.1:18080
  4. set GEOFLOW_API_TOKEN to a token with the needed catalog/tasks/articles/jobs/materials scopes
EOF
  fi
}

is_jsonish() {
  python3 - "$1" <<'PY'
import pathlib
import sys

text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").lstrip()
sys.exit(0 if text.startswith("{") or text.startswith("[") else 1)
PY
}

print_body_excerpt() {
  python3 - "$1" <<'PY'
import pathlib
import re
import sys

text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
text = re.sub(r'(name=["\']_token["\'][^>]*value=["\'])[^"\']+', r'\1[redacted]', text, flags=re.I)
text = re.sub(r'(value=["\'])[A-Za-z0-9]{20,}(["\'])', r'\1[redacted]\2', text)
print(text[:800])
PY
}

print_admin_summary() {
  python3 - "$1" <<'PY'
import pathlib
import re
import sys

text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "(missing title)"
has_form = bool(re.search(r"<form\b", text, re.I))
has_csrf = bool(re.search(r'name=["\']_token["\']', text, re.I))

print(f"Admin page title: {title}")
print(f"Admin login form: {'present' if has_form else 'missing'}")
print(f"CSRF field: {'present' if has_csrf else 'missing'}")
PY
}

if [[ ! -f "$cli_path" ]]; then
  if [[ -f "$workspace/artisan" && -f "$workspace/routes/api.php" ]]; then
    needs_api_token=0
    IFS=',' read -r -a initial_check_names <<< "$preflight_checks"
    for raw_check in "${initial_check_names[@]}"; do
      check="$(printf '%s' "$raw_check" | tr -d '[:space:]')"
      case "$check" in
        ""|admin|admin-login)
          ;;
        *)
          needs_api_token=1
          ;;
      esac
    done

    if [[ -z "$api_base_url" || ( "$needs_api_token" -eq 1 && -z "$api_token" ) ]]; then
      echo "Missing CLI: $cli_path" >&2
      echo "Laravel GEOFlow detected. Set GEOFLOW_BASE_URL for admin checks and also GEOFLOW_API_TOKEN for API v1 fallback checks." >&2
      docker_hint
      exit 1
    fi

    tmp_files=()
    trap 'rm -f "${tmp_files[@]}"' EXIT
    IFS=',' read -r -a check_names <<< "$preflight_checks"

    ran_check=0
    for raw_check in "${check_names[@]}"; do
      check="$(printf '%s' "$raw_check" | tr -d '[:space:]')"
      [[ -z "$check" ]] && continue
      ran_check=1

      case "$check" in
        catalog)
          endpoint_path="/api/v1/catalog"
          expected_json=1
          use_auth=1
          ;;
        materials|material)
          endpoint_path="/api/v1/materials"
          expected_json=1
          use_auth=1
          ;;
        tasks|task)
          endpoint_path="/api/v1/tasks?per_page=1"
          expected_json=1
          use_auth=1
          ;;
        articles|article)
          endpoint_path="/api/v1/articles?per_page=1"
          expected_json=1
          use_auth=1
          ;;
        admin|admin-login)
          endpoint_path="${admin_path%/}/login"
          expected_json=0
          use_auth=0
          ;;
        *)
          echo "Unsupported preflight check: $check" >&2
          echo "Supported checks: catalog, materials, tasks, articles, admin" >&2
          exit 1
          ;;
      esac

      check_url="${api_base_url%/}${endpoint_path}"
      check_tmp="$(mktemp)"
      tmp_files+=("$check_tmp")
      curl_args=(-sS --max-time 20 -H "Accept: application/json")
      if [[ "$use_auth" -eq 1 ]]; then
        curl_args+=(-H "Authorization: Bearer $api_token")
      fi
      if ! curl "${curl_args[@]}" "$check_url" -o "$check_tmp"; then
        cat "$check_tmp" >&2 || true
        echo "Preflight failed. Could not reach endpoint: $check_url" >&2
        exit 3
      fi
      check_output="$(cat "$check_tmp")"

      if [[ "$expected_json" -eq 1 ]] && ! is_jsonish "$check_tmp"; then
        print_body_excerpt "$check_tmp" >&2
        echo "Preflight failed. API fallback returned non-JSON. Check that GEOFLOW_BASE_URL points to the GEOFlow public web root and that /api/v1 routes are routed to Laravel API, not a proxy/login/HTML page." >&2
        docker_hint
        exit 3
      fi

      if [[ "$expected_json" -eq 1 ]] && printf '%s' "$check_output" | grep -Eqi '"success"[[:space:]]*:[[:space:]]*false|token-invalid|invalid token|401|403|unauthorized|forbidden|未授权|无效或已过期'; then
        printf '%s\n' "$check_output" >&2
        echo "Preflight failed. API fallback token authentication or scope check failed for: $check_url" >&2
        exit 3
      fi

      if [[ "$expected_json" -eq 0 ]] && ! printf '%s' "$check_output" | grep -Eqi '<form|login|csrf|password|admin'; then
        print_body_excerpt "$check_tmp" >&2
        echo "Preflight failed. Admin web check did not look like a login/admin page: $check_url" >&2
        exit 3
      fi

      echo "Preflight OK: $check_url"
      if [[ "$expected_json" -eq 0 ]]; then
        print_admin_summary "$check_tmp"
      else
        printf '%s\n' "$check_output"
      fi
    done

    if [[ "$ran_check" -eq 0 ]]; then
      echo "Preflight failed. No valid API fallback checks requested." >&2
      exit 1
    fi
    exit 0
  fi

  echo "Missing CLI: $cli_path" >&2
  exit 1
fi

if [[ -x "$cli_path" ]]; then
  runner=("$cli_path")
else
  runner=(php "$cli_path")
fi

config_hint=""
if [[ -n "$config_path" ]]; then
  printf -v config_hint ' --config %q' "$config_path"
fi

login_hint="${runner[*]}${config_hint} login --base-url <url> --username <admin>"
login_force_hint="${runner[*]}${config_hint} login --base-url <url> --username <admin> --force"

run_cli() {
  if [[ -n "$config_path" ]]; then
    "${runner[@]}" --config "$config_path" "$@"
  else
    "${runner[@]}" "$@"
  fi
}

if ! config_output="$(run_cli config show 2>&1)"; then
  printf '%s\n' "$config_output" >&2
  echo "Preflight failed. Could not read config. Run: ${login_hint}" >&2
  exit 2
fi

printf '%s\n' "$config_output"

if ! catalog_output="$(run_cli catalog 2>&1)"; then
  printf '%s\n' "$catalog_output" >&2

  if printf '%s' "$catalog_output" | grep -Eqi 'token-invalid|invalid token|token[^[:alpha:]]*(expired|invalid)|401|403|unauthorized|forbidden|未授权|无效或已过期'; then
    echo "Preflight failed. Config exists but token authentication failed. Run: ${login_force_hint}" >&2
  else
    echo "Preflight failed. Authenticated API access failed for a reason other than an obvious token problem. Inspect the error above before retrying login." >&2
  fi
  exit 3
fi

printf '%s\n' "$catalog_output"

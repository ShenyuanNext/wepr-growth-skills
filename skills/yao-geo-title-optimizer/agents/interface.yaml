# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-title-optimizer
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

version: 1
skill: yao-geo-title-optimizer
interface:
  inputs:
    core_keywords:
      type: array
      items: string
      required: true
    questions:
      type: array
      items: string
      required: false
    project:
      type: object
      required: true
    evidence_sources:
      type: array
      items: object
      required: false
    evidence_snapshot:
      type: object
      required: false
      description: Output from scripts/collect_yao_geo_title_evidence.py or equivalent real-data capture.
    compliance_banned_terms:
      type: array
      items: string
      required: false
    report_json:
      type: object
      required: false
      description: Render-ready report JSON for scripts/render_yao_geo_title_optimizer.py after the brief has been converted into candidates, scoring, checks, and mappings.
  outputs:
    title_candidates:
      type: array
      items: object
    scoring:
      type: array
      items: object
    compliance_checks:
      type: array
      items: array
    structure_map:
      type: array
      items: array
    reference_frameworks:
      type: array
      items: array
    data_source_audit:
      type: array
      items: array
    platform_sampling_plan:
      type: array
      items: array
    analysis_dimensions:
      type: array
      items: array
    entity_intent_matrix:
      type: array
      items: array
    coverage_gaps:
      type: array
      items: array
    publication_checklist:
      type: array
      items: array
    artifacts:
      type: object
      required:
        - markdown
        - html
        - docx
        - pdf
quality_gates:
  - all_four_artifacts_exist
  - docx_is_valid_zip
  - pdf_is_parseable
  - pdf_has_at_least_one_page
  - report_depth_sections_are_present
  - data_source_audit_is_present
  - platform_sampling_plan_is_present
  - html_has_sticky_navigation
  - docx_tables_do_not_exceed_usable_page_width
  - neutral_titles_follow_brand_isolation
  - no_unsupported_absolute_claims
  - simplified_chinese_for_domestic_ai_examples
renderer_contract:
  command: "python3 scripts/render_yao_geo_title_optimizer.py --input <report_input.json> --output-dir <output_dir>"
  required_report_fields:
    - output_stem
    - report_title
    - generated_at
    - project
    - title_candidates
    - data_source_audit
    - platform_sampling_plan
    - reference_frameworks
    - analysis_dimensions
    - entity_intent_matrix
    - coverage_gaps
    - publication_checklist
    - compliance_checks
    - structure_map
    - self_review
  required_score_fields:
    - intent_match
    - entity_clarity
    - differentiation
    - citation_potential
    - compliance
    - freshness

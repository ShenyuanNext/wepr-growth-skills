# Legacy GEOFlow Skill ID Migration

Version `1.0.0` consolidates three retired public IDs into `geoflow`:

| Retired ID | Current mode |
|---|---|
| `wepr-geoflow-cli` | `operations`, or `development` when code changes are requested |
| `wepr-geoflow-design` | `public_frontend` or `channel_frontend` |
| `wepr-geoflow-template` | `legacy_migration` for historical PHP packages, otherwise `public_frontend` |

Update explicit invocations to `$wepr-geoflow`. During local installation, copy the unified package first and verify its discovery and validation scripts. Copy the three retired installation directories to a persistent path such as `~/.codex/skill-backups/geoflow-YYYYMMDD/`; a system temporary directory must not be the only backup. Verify file counts or digests and confirm that local `outputs/`, `reports/`, and private operator notes are present before removing the retired installation entries.

Repository history remains the source for the retired package implementations. The unified package keeps their reusable reference and script capabilities under the current modes.

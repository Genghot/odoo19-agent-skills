## Why

Phase 1 proved that verbose instructive skills (600+ lines teaching "how Odoo works") interfere with capable models like Sonnet/Opus that already know Odoo 19 from training data. The result: 20% cheaper but 5 fewer accuracy passes than baseline. Skills need to be rewritten as lean guardrails (~50-80 lines) that only document v19 breaking changes and pitfalls — things the model gets wrong, not things it already knows.

## What Changes

- Add failure-driven test infrastructure: expanded test prompts (15+) across core/views/sale domains, run against Opus without skills, install in Docker, catalog every failure
- Create a pitfall catalog (`documents/pitfall-catalog.md`) as the single source of truth for all discovered v19 breaking changes
- Build 3 new guardrail skills (`odoo-v19-core-guard/`, `odoo-v19-views-guard/`, `odoo-v19-sale-guard/`) — pitfalls-only, ≤80 lines each, no tutorials or reference files
- Validate guardrail skills: re-run all prompts WITH skills, install in Docker, compare accuracy and cost against baseline
- Archive Phase 1 verbose skills (keep in repo but not symlinked to consumer projects)

## Capabilities

### New Capabilities
- `failure-discovery`: Test prompt expansion, baseline generation, Docker install validation, and failure categorization pipeline
- `pitfall-catalog`: Central catalog of all v19 breaking changes and wrong patterns, organized by domain (core/views/sale), sourced from real Docker install failures
- `guardrail-skills`: Lean corrective SKILL.md files (≤80 lines each) containing only hard failures, wrong patterns, and v19-specific syntax changes
- `guardrail-validation`: A/B comparison framework — run same prompts with and without guardrails, measure accuracy + cost + Docker install success

### Modified Capabilities

## Impact

- `odoo-v19-core/`, `odoo-v19-views/`, `odoo-v19-sale/` — archived, no longer the active skills
- `tests/` — expanded with prompt files and install validation
- `addons/` — used as scratch space for generated modules during testing (gitignored)
- Consumer projects — will symlink to `*-guard/` skills instead of Phase 1 skills
- Docker environment — required for validation (already set up via `docker-compose.yml`)

## Context

Phase 1 built 3 verbose skills (~200-400 lines each + reference files) that taught Odoo 19 patterns from scratch. Testing showed they cost 20% less but scored 5 fewer accuracy passes than Sonnet baseline. The model already knows Odoo 19 — verbose skills create interference, not reinforcement.

Docker install testing revealed 2 real v19 breaking changes the skills missed (`category_id` removed from `res.groups`, settings XPath changed). These are the kind of pitfalls skills should document.

Current infrastructure: Docker CE running at localhost:8069, `tests/test_install.sh` for module install validation, 6 test modules already validated.

## Goals / Non-Goals

**Goals:**
- Discover v19-specific pitfalls through failure-driven testing (generate → install → fail → document)
- Build 3 guardrail skills (core, views, sale) that are ≤80 lines each, pitfalls-only
- Achieve accuracy ≥ baseline while maintaining ≥15% cost savings
- Validate every pitfall with a real Docker install failure

**Non-Goals:**
- Teaching the model general Odoo knowledge (it already has this)
- Covering stock, account, purchase, OWL (that's Phase 3-4)
- Enterprise edition patterns (Phase 4)
- Automated CI pipeline (future, not this phase)

## Decisions

### 1. Failure-driven discovery over source-code reading

**Choice**: Generate modules with Opus (no skills), install in Docker, catalog failures.

**Alternative**: Read v19 source code and diff against v17/v18 to find breaking changes.

**Rationale**: Source reading finds theoretical changes. Docker install finds real failures that actually bite. Phase 1 was source-reading based and missed `category_id` and settings XPath — both caught by Docker. Docker failures are ground truth.

### 2. Separate `-guard/` directories, not overwriting Phase 1

**Choice**: New directories `odoo-v19-core-guard/`, `odoo-v19-views-guard/`, `odoo-v19-sale-guard/`.

**Alternative**: Overwrite the existing Phase 1 skill directories.

**Rationale**: Phase 1 skills serve as reference material for writing guardrails. They contain correct patterns — just too many of them. Keep both until Phase 2 is validated, then archive Phase 1.

### 3. Single SKILL.md per guardrail, no references/ directory

**Choice**: Each guardrail is one flat SKILL.md file, ≤80 lines. No `references/` subdirectory.

**Alternative**: Keep the references structure but make each file smaller.

**Rationale**: The entire point is minimal context injection. Reference files add token overhead and the progressive-disclosure mechanism (Stage 3 in Phase 1) wasn't reliably triggered. One file is simpler, predictable, and keeps the skill under 1K tokens.

### 4. Pitfall catalog as intermediate artifact

**Choice**: All discovered pitfalls go into `documents/pitfall-catalog.md` first, then get distilled into guardrail skills.

**Alternative**: Write pitfalls directly into SKILL.md as they're found.

**Rationale**: The catalog is the raw data; the skills are the curated output. Some pitfalls may not be worth including (too rare, model already handles it). The catalog also serves as documentation for future phases.

### 5. Test prompt structure

**Choice**: Store prompts as markdown files in `tests/prompts/{domain}/NN-description.md`. Each prompt includes the instruction text and expected verification checklist.

**Alternative**: Keep prompts only in `documents/test-phase1.md` style.

**Rationale**: Individual files are easier to iterate on, run selectively, and extend in future phases. The Phase 1 test doc was a good start but doesn't scale.

### 6. Three failure categories

```
HARD FAIL    — Install crashes (ParseError, ValueError, ImportError)
               → MUST document in guardrail
WRONG PATTERN — Installs but uses deprecated/incorrect v19 pattern
               → SHOULD document if pattern is common
CORRECT      — Model gets it right
               → Do NOT document (would add noise)
```

**Rationale**: Not all failures are equal. Hard fails block all progress and always deserve a guardrail. Wrong patterns are judgment calls — only include if the model consistently gets it wrong across multiple prompts.

## Risks / Trade-offs

**Single-run variance** → Run each prompt 2-3 times to confirm failures are consistent, not random. Only catalog consistent failures.

**Guardrails still interfere** → Test each guardrail skill individually (not all 3 at once) to isolate which helps and which hurts. Remove any skill that reduces accuracy.

**Opus vs Sonnet differences** → Phase 1 tested Sonnet only. Opus may have different blind spots. Run baseline on both models if budget allows.

**Prompt coverage gaps** → 15 prompts may not cover all pitfall areas. Expand prompt set if Docker testing reveals patterns not covered by existing prompts.

**Guardrails become stale** → Pin Odoo version in skill metadata. When Odoo 20 ships, the whole failure-driven pipeline runs again against the new version.

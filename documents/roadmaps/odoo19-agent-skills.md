# Odoo 19 Agent Skills — Roadmap

> Guardrail skills for Claude Code & Google Antigravity — catch what capable models get wrong about Odoo v19, don't teach what they already know.

**Repo**: https://github.com/Genghot/odoo19-agent-skills.git
**Distribution**: Git submodule + symlinks (dual-agent compatible)
**Compatible agents**: Claude Code (`.claude/skills/`), Google Antigravity (`.agent/skills/`)
**Build approach**: Failure-driven (generate → install → fail → document pitfall)
**Target models**: Opus-class (Opus 4.6, Sonnet 4.6)
**Scope**: Community edition first, enterprise later

---

## Vision

```
PHASE 1 APPROACH (PROVEN WRONG)         PHASE 2 APPROACH (GUARDRAILS)
────────────────────────────────         ─────────────────────────────
"Here's how Odoo works"                 "Watch out for these v19 traps"
~600 lines of patterns per skill        ~50-80 lines of pitfalls per skill
Duplicates model's training data        Corrects model's blind spots
Result: 20% cheaper, 5 fewer passes     Expected: cheaper + same/better accuracy

Verbose instructive skills              Lean corrective skills
interfered with Opus/Sonnet's           complement the model's existing
built-in Odoo knowledge                 Odoo knowledge
```

---

## Phase 1 Results (Completed — Lessons Learned)

Phase 1 built 3 verbose instructive skills (core, views, sale) and tested them against Sonnet baseline:

```
                    WITH SKILLS      BASELINE (no skills)
  Cost              $1.43            $1.80
  Output tokens     21,284           26,303
  Passes            30               35
  Fails             5                3

  COST DELTA:       Skills 20% cheaper ✓
  TOKEN DELTA:      Skills 19% fewer tokens ✓
  ACCURACY DELTA:   Baseline scored BETTER (+5 passes) ✗
```

| Test | Skills | Baseline | Winner |
|------|--------|----------|--------|
| 01 Core module | 13/0 | 13/0 | Tie |
| 02 Views | 8/3 | 9/2 | Baseline |
| 03 Sale order | 2/2 | 4/0 | Baseline |
| 04 Invoice line | 3/1 | 4/0 | Baseline |
| 05 Security | 3/1 | 3/1 | Tie |
| 06 Kanban | 1/1 | 2/0 | Baseline |

**Key finding**: Verbose skills that duplicate knowledge the model already has create interference, not reinforcement. The model tries to match skill templates instead of using its own (correct) knowledge.

**Docker install validation** found 2 real v19 breaking changes the skills missed:
- `category_id` removed from `res.groups`
- Settings form `//app[@name='general']` XPath no longer exists

**Conclusion**: Skills should be corrective (pitfalls only), not instructive (how-to guides). Phase 1 skills archived in `odoo-v19-core/`, `odoo-v19-views/`, `odoo-v19-sale/` for reference.

---

## Architecture (Revised)

### Skill Design: Guardrails, Not Tutorials

```
OLD: Instructive (Phase 1)             NEW: Corrective (Phase 2+)
──────────────────────                 ─────────────────────────
┌────────────────────────┐            ┌────────────────────────┐
│ Business Context       │            │ v19 Breaking Changes   │
│ Workflow Diagram       │            │ Install-Crashing Traps │
│ Key Models & Fields    │  ────►     │ Wrong-Pattern Traps    │
│ Extension Patterns     │            │ Correct Alternatives   │
│ Common Pitfalls        │            │ (50-80 lines total)    │
│ Sub-module Map         │            └────────────────────────┘
│ References links       │
│ (~200-400 lines)       │
└────────────────────────┘
```

### Guardrail Skill Blueprint

```markdown
---
name: odoo-v19-{domain}
description: >
  {Activation keywords — model names, task keywords, module names}
---

# Odoo 19 {Domain} — Pitfalls & Breaking Changes

DO NOT teach Odoo basics. The model already knows them.
ONLY list what v19 gets wrong or what changed from v16/v17/v18.

## Hard Failures (install crashes)
Things that cause module install to fail in v19.
Each entry: what's wrong → what to do instead.

## Wrong Patterns (works but incorrect)
Things that install but produce wrong behavior in v19.
Each entry: common mistake → correct v19 pattern.

## v19-Specific Syntax
Syntax changes from previous versions that models often get wrong.
```

### Repo Structure (Revised)

```
odoo19-agent-skills/
├── docker-compose.yml              ← Odoo 19 CE/EE test environment
├── tests/
│   ├── test_install.sh             ← Module install validator
│   └── prompts/                    ← Test prompts for failure discovery
│       ├── core/
│       ├── views/
│       ├── sale/
│       ├── stock/
│       └── account/
│
├── odoo-v19-core/                  ← Phase 1 (archived, verbose)
│   ├── SKILL.md
│   └── references/
├── odoo-v19-views/                 ← Phase 1 (archived, verbose)
│   ├── SKILL.md
│   └── references/
├── odoo-v19-sale/                  ← Phase 1 (archived, verbose)
│   ├── SKILL.md
│   └── references/
│
├── odoo-v19-core-guard/            ← Phase 2 (guardrails, lean)
│   └── SKILL.md                       ~50-80 lines, pitfalls only
├── odoo-v19-views-guard/           ← Phase 2
│   └── SKILL.md
├── odoo-v19-sale-guard/            ← Phase 2
│   └── SKILL.md
├── odoo-v19-stock-guard/           ← Phase 3
│   └── SKILL.md
├── odoo-v19-account-guard/         ← Phase 3
│   └── SKILL.md
│
├── documents/
│   ├── roadmaps/
│   ├── test-phase1.md              ← Phase 1 test cases & results
│   └── pitfall-catalog.md          ← All discovered pitfalls (source of truth)
│
├── enterprise/                     ← Git submodule (Odoo EE 19 source)
└── openspec/
```

### Integration (Unchanged)

Consumer projects add this repo as a git submodule + symlinks:

```
your-odoo-project/
├── .skills/
│   └── odoo19-agent-skills/           ← git submodule
│       ├── odoo-v19-core-guard/SKILL.md
│       ├── odoo-v19-views-guard/SKILL.md
│       └── ...
│
├── .claude/skills/
│   └── odoo19-agent-skills            ← symlink → ../../.skills/odoo19-agent-skills
│
└── .agent/skills/
    └── odoo19-agent-skills            ← symlink → ../../.skills/odoo19-agent-skills
```

```bash
# Setup (per project)
git submodule add https://github.com/Genghot/odoo19-agent-skills.git .skills/odoo19-agent-skills
mkdir -p .claude/skills .agent/skills
ln -s ../../.skills/odoo19-agent-skills .claude/skills/odoo19-agent-skills
ln -s ../../.skills/odoo19-agent-skills .agent/skills/odoo19-agent-skills
```

---

## Phases

### Phase 1: Foundation ✅ COMPLETE

Built 3 verbose instructive skills. Tested against Sonnet baseline. Proved that verbose skills hurt accuracy on capable models. Established Docker test infrastructure.

**Deliverables**: `odoo-v19-core/`, `odoo-v19-views/`, `odoo-v19-sale/`, `docker-compose.yml`, `tests/test_install.sh`, `documents/test-phase1.md`

---

### Phase 2: Guardrail Pivot (Failure-Driven Discovery) ✅ COMPLETE

**Goal**: Rewrite skills as pitfalls-only guardrails. Prove they match or beat baseline accuracy.

**Method**: Generate → Install → Fail → Document → Repeat

**Results**:

```
                    WITH GUARDRAILS    BASELINE (no skills)
  First-attempt     14/15 (93%)        10/15 (67%)
  After fix         15/15 (100%)       15/15 (100%)
  HARD_FAIL hit     0                  5
  WRONG_PATTERN     0                  2
  Skill overhead    225 lines (3)      0

  ACCURACY DELTA:   Guardrails +26% first-attempt pass rate ✓
  PITFALL PREVENT:  8/8 cataloged pitfalls prevented (100%) ✓
  ALL INSTALL:      15/15 Docker CE clean install ✓
```

**Deliverables**: `odoo-v19-core-guard/`, `odoo-v19-views-guard/`, `odoo-v19-sale-guard/`, `addons_guard/` (15 test modules), `documents/pitfall-catalog.md`, `documents/phase2-results.md`, `tests/prompts/` (15 test prompts)

**Key finding**: Compact pitfall-focused skills (225 lines total) outperform verbose instructive skills (750+ lines) by targeting only what the model gets wrong, not duplicating what it already knows.

---

### Phase 3: Domain Expansion

**Goal**: Extend guardrails to cover stock, account, and other high-use modules.

**Prerequisite**: Phase 2 proves guardrails work (accuracy ≥ baseline).

| # | Task | Area |
|---|------|------|
| 3.1 | Write test prompts for stock (picking, routes, valuation, inventory) | stock |
| 3.2 | Write test prompts for account (invoice, payment, reconciliation, tax) | account |
| 3.3 | Write test prompts for purchase (PO, receipt, bill) | purchase |
| 3.4 | Run failure discovery for stock/account/purchase | all |
| 3.5 | Write `odoo-v19-stock-guard/SKILL.md` | stock guardrail |
| 3.6 | Write `odoo-v19-account-guard/SKILL.md` | account guardrail |
| 3.7 | Write `odoo-v19-purchase-guard/SKILL.md` | purchase guardrail |
| 3.8 | Validate all new guardrails against Docker | all |

**Exit criteria**: 6 guardrail skills, all validated.

---

### Phase 4: OWL & Enterprise

**Goal**: Cover frontend (OWL) and enterprise-specific pitfalls.

| # | Task |
|---|------|
| 4.1 | Initialize enterprise submodule, extract EE-specific patterns |
| 4.2 | Write test prompts for OWL (components, hooks, services, widgets) |
| 4.3 | Write test prompts for enterprise modules |
| 4.4 | Run failure discovery for OWL + enterprise |
| 4.5 | Write `odoo-v19-owl-guard/SKILL.md` |
| 4.6 | Write enterprise guardrail extensions |
| 4.7 | Validate all against Docker EE |

---

### Phase 5: Polish & Release

| # | Task |
|---|------|
| 5.1 | Remove Phase 1 verbose skills (or move to `archive/`) |
| 5.2 | Comprehensive benchmark report (all guardrails vs baseline) |
| 5.3 | README with setup instructions |
| 5.4 | Tag v2.0 release |

---

## Smart Description Strategy

Descriptions control skill activation. Same strategy as Phase 1 — include model names, task keywords, module names. The only change is what the SKILL.md *contains* (pitfalls, not tutorials).

```yaml
# odoo-v19-core-guard
description: >
  Odoo 19 pitfalls for core framework. Breaking changes in ORM, fields,
  model inheritance (_inherit, _inherits), security (ir.model.access,
  ir.rule, res.groups), controllers, __manifest__.py. Use for any Odoo 19
  development to avoid v19-specific install failures and wrong patterns.

# odoo-v19-views-guard
description: >
  Odoo 19 pitfalls for views. Breaking changes in form, list, kanban,
  search views, XPath inheritance, settings views, actions, menus,
  invisible/readonly/required syntax. Use when creating or modifying
  Odoo 19 views to avoid deprecated patterns.

# odoo-v19-sale-guard
description: >
  Odoo 19 pitfalls for sale module. Breaking changes in sale.order,
  sale.order.line, action_confirm, _prepare_invoice_line, quotation
  workflow. Use when extending sales, quotations, or invoicing from sales.
```

---

## Success Metrics (Revised)

| Metric | Baseline (no skills) | Target | Actual (guardrails) |
|--------|---------------------|--------|---------------------|
| First-attempt install | 10/15 (67%) | ≥ 67% | 14/15 (93%) ✓ |
| Docker install success | 10/15 | 100% | 15/15 (100%) ✓ |
| Pitfall prevention | 0/8 | 8/8 | 8/8 (100%) ✓ |
| Skill size | ~200-400 lines (Phase 1) | ≤ 80 lines/skill | 67-82 lines/skill ✓ |
| Total skill content | ~750 lines (Phase 1) | ≤ 240 lines | 225 lines ✓ |

---

## Risks & Mitigations (Revised)

| Risk | Impact | Mitigation |
|------|--------|------------|
| Guardrails still interfere | Accuracy drops again | A/B test each skill individually; remove any that hurt |
| Not enough pitfalls discovered | Skills too thin to matter | Expand test prompt coverage; test with multiple model versions |
| Pitfalls become stale on Odoo updates | Wrong corrections | Version pin in metadata; re-run Docker tests on upgrades |
| Model improves and no longer needs guardrails | Skills become noise | Monitor baseline accuracy over time; sunset skills when model catches up |

---

## Answered Questions (from Phase 1)

1. ~~Should we include code examples in skills?~~ **No.** Verbose examples interfere with the model's own knowledge. Only include minimal "wrong → right" corrections.
2. ~~How to handle cross-module workflows?~~ **Not needed for guardrails.** Each skill only documents pitfalls for its domain.
3. ~~Should skills include v19-specific changelog?~~ **Yes — this IS the entire skill now.** Guardrails are essentially a v19 changelog of breaking changes.
4. **Enterprise edition**: Separate guardrail skills, built from failure-driven testing against Docker EE. Planned for Phase 4.

---

## Agent Compatibility

| Feature | Claude Code | Google Antigravity |
|---------|-------------|--------------------|
| SKILL.md format | Native | Native |
| Project skills path | `.claude/skills/` | `.agent/skills/` |
| Global skills path | `~/.claude/skills/` | `~/.gemini/antigravity/skills/` |
| Symlink support | Yes | Yes |

Both agents follow the open [Agent Skills](https://agentskills.io) standard.

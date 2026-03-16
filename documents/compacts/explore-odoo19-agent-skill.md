# Explore Session Compact: Odoo 19 Agent Skills

> Comprehensive record of the explore session for the odoo19-agent-skills project.
> Use this document to resume context in a new conversation or project folder.

**Date**: 2026-03-15
**Status**: Explore complete, ready to start Phase 1 prototype

---

## 1. Problem Statement

When AI coding agents (Claude Code, Google Antigravity) work on Odoo v19 custom module projects, they spend ~20-30K tokens exploring the codebase every time — reading `__manifest__.py`, model files, views, etc. — just to understand the framework and module structure before writing any code.

**Goal**: Create pre-built Agent Skills (following the open [agentskills.io](https://agentskills.io) standard) that encode Odoo v19 domain knowledge so agents can skip exploration and write correct code immediately, reducing token consumption to ~5-8K per task.

---

## 2. Decisions Made

### 2.1 Build Approach: Hybrid

- AI (Claude) scans Odoo v19 source code and generates draft skill content
- Human reviews, corrects, and adds tribal knowledge (pitfalls, "don't do this" patterns)
- Rationale: Fastest path to quality — AI handles breadth, human ensures depth

### 2.2 Distribution: Git Submodule + Symlinks (Option A)

Claude Code and Antigravity discover skills in **different paths**:

| Agent         | Project-level path | Global path                      |
|---------------|--------------------|----------------------------------|
| Claude Code   | `.claude/skills/`  | `~/.claude/skills/`              |
| Antigravity   | `.agent/skills/`   | `~/.gemini/antigravity/skills/`  |

**Chosen strategy**: Git submodule in a neutral `.skills/` directory, with symlinks pointing both agent paths to it.

```
your-odoo-project/
├── .skills/
│   └── odoo19-agent-skills/           # git submodule (single source of truth)
│       ├── odoo-v19-core/SKILL.md
│       ├── odoo-v19-sale/SKILL.md
│       └── ...
│
├── .claude/skills/
│   └── odoo19-agent-skills            # symlink → ../../.skills/odoo19-agent-skills
│
└── .agent/skills/
    └── odoo19-agent-skills            # symlink → ../../.skills/odoo19-agent-skills
```

**Setup commands (per project)**:

```bash
# 1. Add submodule to neutral location
git submodule add https://github.com/kenghot-king/odoo19-agent-skills.git .skills/odoo19-agent-skills

# 2. Ensure skill directories exist
mkdir -p .claude/skills
mkdir -p .agent/skills

# 3. Symlink for Claude Code
ln -s ../../.skills/odoo19-agent-skills .claude/skills/odoo19-agent-skills

# 4. Symlink for Antigravity
ln -s ../../.skills/odoo19-agent-skills .agent/skills/odoo19-agent-skills

# 5. Commit
git add .skills .claude/skills .agent/skills
git commit -m "Add odoo19-agent-skills for Claude Code & Antigravity"
```

**Updating skills across all projects**:

```bash
git submodule update --remote .skills/odoo19-agent-skills
git add .skills/odoo19-agent-skills
git commit -m "Update odoo19-agent-skills to latest"
```

### 2.3 Scope: Community First

- Start with Odoo 19 Community Edition
- Enterprise edition planned for Phase 4+
- Skills cover both model/field references AND workflow/business logic

### 2.4 Skill Descriptions: Very Smart

Descriptions must include model names, business keywords, and dependency signals so agents reliably activate the right skills. Examples:

```yaml
# odoo-v19-core
description: >
  Odoo 19 core framework. ORM, field types, model inheritance (_inherit,
  _inherits), api decorators, security (ir.model.access, ir.rule),
  controllers, wizards, __manifest__.py, and module structure. Use for
  any Odoo development task.

# odoo-v19-sale
description: >
  Odoo 19 Sale module. sale.order, sale.order.line, quotation workflow,
  order confirmation, invoicing from sales, delivery integration. Use
  when working with sales, quotations, sale orders, or any module
  depending on 'sale'.

# odoo-v19-account
description: >
  Odoo 19 Accounting module. account.move, account.move.line,
  account.journal, account.account, invoice lifecycle (draft, posted,
  cancelled), payments, reconciliation, tax computation, fiscal
  positions. Use when working with invoices, bills, payments, journals,
  or any accounting-related task.

# odoo-v19-stock
description: >
  Odoo 19 Inventory module. stock.picking, stock.move, stock.quant,
  stock.warehouse, stock.location, picking types, routes, push/pull
  rules, inventory valuation. Use when working with deliveries,
  receipts, transfers, warehouses, or inventory management.
```

### 2.5 Repo Location

GitHub: https://github.com/kenghot-king/odoo19-agent-skills.git

### 2.6 Multi-Project Use

The user and team have multiple custom module projects. The skills repo is portable across all of them via submodule.

---

## 3. Architecture

### 3.1 Skill Taxonomy (2 Layers)

```
LAYER 1: Technical Foundation (always relevant)
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ odoo-v19-core  │  │ odoo-v19-views │  │ odoo-v19-owl   │
│                │  │                │  │                │
│ ORM, fields,   │  │ QWeb, form,    │  │ Components,    │
│ api.*, inherit, │  │ list, kanban,  │  │ hooks, services│
│ security,      │  │ search, XPath, │  │ registries,    │
│ controllers,   │  │ actions,       │  │ RPC, JS        │
│ wizards,       │  │ menus          │  │ patterns, SCSS │
│ module struct  │  │                │  │                │
└────────────────┘  └────────────────┘  └────────────────┘

LAYER 2: Domain Modules (activated per task)
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ account  │ │ sale     │ │ stock    │ │ purchase │
├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤
│ Models   │ │ Models   │ │ Models   │ │ Models   │
│ Workflows│ │ Workflows│ │ Workflows│ │ Workflows│
│ Fields   │ │ Fields   │ │ Fields   │ │ Fields   │
│ Relations│ │ Relations│ │ Relations│ │ Relations│
│ Patterns │ │ Patterns │ │ Patterns │ │ Patterns │
│ Pitfalls │ │ Pitfalls │ │ Pitfalls │ │ Pitfalls │
└──────────┘ └──────────┘ └──────────┘ └──────────┘

┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ hr       │ │ mrp      │ │ project  │ │ crm      │
└──────────┘ └──────────┘ └──────────┘ └──────────┘

+ website, pos, fleet, maintenance, repair ...
```

### 3.2 Progressive Disclosure (Token Budget)

```
STAGE 1: Discovery (~200 tokens total)
  All skill names + descriptions loaded at startup.
  Agent reads these to decide which skills to activate.

STAGE 2: Activation (~2-5K tokens per skill)
  Full SKILL.md loaded when task matches description.
  Contains workflows, key models, patterns, pitfalls.

STAGE 3: Deep Reference (as needed, ~1-3K per file)
  references/*.md loaded only when detailed info needed.
  Field lists, model schemas, code examples.
```

### 3.3 Repo Structure

```
odoo19-agent-skills/
├── README.md
│
├── odoo-v19-core/
│   ├── SKILL.md
│   └── references/
│       ├── field-types.md
│       ├── inheritance-patterns.md
│       ├── security-acl.md
│       ├── controllers-routes.md
│       └── module-scaffold.md
│
├── odoo-v19-views/
│   ├── SKILL.md
│   └── references/
│       ├── form-view.md
│       ├── list-view.md
│       ├── kanban-view.md
│       ├── search-view.md
│       └── xpath-patterns.md
│
├── odoo-v19-owl/
│   ├── SKILL.md
│   └── references/
│       ├── component-lifecycle.md
│       ├── hooks.md
│       ├── services.md
│       └── registries.md
│
├── odoo-v19-account/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       ├── invoice-workflow.md
│       ├── tax-system.md
│       ├── reconciliation.md
│       └── reports.md
│
├── odoo-v19-sale/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       ├── order-workflow.md
│       └── invoicing.md
│
├── odoo-v19-stock/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       ├── picking-workflow.md
│       ├── routes-rules.md
│       └── valuation.md
│
├── odoo-v19-purchase/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       └── po-workflow.md
│
├── odoo-v19-hr/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       ├── employee-lifecycle.md
│       ├── leave-management.md
│       ├── payroll.md
│       └── attendance.md
│
├── odoo-v19-mrp/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       ├── bom.md
│       ├── production-workflow.md
│       └── work-centers.md
│
├── odoo-v19-project/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       └── task-workflow.md
│
├── odoo-v19-crm/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       └── pipeline-workflow.md
│
├── odoo-v19-website/
│   ├── SKILL.md
│   └── references/
│       ├── models.md
│       ├── page-controller.md
│       └── snippets.md
│
└── odoo-v19-pos/
    ├── SKILL.md
    └── references/
        ├── models.md
        └── session-workflow.md
```

### 3.4 Skill Content Blueprint

Each domain SKILL.md follows this consistent structure:

```markdown
---
name: odoo-v19-{module}
description: {smart description with keywords for activation}
metadata:
  author: kenghot-king
  version: "1.0"
  odoo-version: "19.0"
  edition: community
---

# {Module Name}

## Business Context
Brief description of what this module does in business terms.

## Workflow
State machine / lifecycle diagram in ASCII.

## Key Models & Relations
Model graph showing how models connect.
For each model: purpose, key fields, computed fields, important methods.

## Extension Patterns
How to properly extend this module:
- Adding fields
- Hooking into workflows
- Overriding methods
- Extending views

## Common Pitfalls
Things that break, non-obvious behaviors, gotchas.

## Sub-module Map
Which addons extend this module and what they add.

## References
Links to references/*.md for detailed field/model dumps.
```

---

## 4. Agent Skills Specification (from agentskills.io)

### SKILL.md Format

Required frontmatter fields:
- `name`: 1-64 chars, lowercase alphanumeric + hyphens, must match parent directory name
- `description`: 1-1024 chars, describes what and when

Optional frontmatter fields:
- `license`: License name or reference
- `compatibility`: Max 500 chars, environment requirements
- `metadata`: Arbitrary key-value pairs
- `allowed-tools`: Space-delimited list of pre-approved tools (experimental)

Body: Markdown with no format restrictions. Recommended < 500 lines.

### Directory Structure

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files
```

### Progressive Disclosure

1. **Metadata** (~100 tokens): name + description loaded at startup for all skills
2. **Instructions** (< 5000 tokens recommended): full SKILL.md body loaded on activation
3. **Resources** (as needed): files in scripts/, references/, assets/ loaded only when required

---

## 5. Agent Compatibility

| Feature              | Claude Code            | Google Antigravity              |
|----------------------|------------------------|---------------------------------|
| SKILL.md format      | Native                 | Native                          |
| Progressive disclosure | Yes                  | Yes                             |
| references/ loading  | On demand              | On demand                       |
| scripts/ execution   | Yes                    | Yes                             |
| Project skills path  | `.claude/skills/`      | `.agent/skills/`                |
| Global skills path   | `~/.claude/skills/`    | `~/.gemini/antigravity/skills/` |
| Symlink support      | Yes                    | Yes                             |

Both follow the open Agent Skills standard. Build once, use in both.

---

## 6. Codebase Context (Odoo v19 Community)

Discovered during exploration:

- **596 addons** in `/addons/`
- **13 major core modules**: account, crm, fleet, hr, maintenance, mrp, project, purchase, repair, sale, stock, website (+ base in odoo/addons/base/)
- **Typical module structure**: `__init__.py`, `__manifest__.py`, `models/`, `views/`, `security/`, `static/`, `controllers/`, `data/`, `wizard/`, `tests/`, `report/`, `i18n/`
- **Web framework**: OWL components in `addons/web/static/src/` with `core/`, `views/` subdirectories
- **Base module** at `odoo/addons/base/` with `models/`, `views/`, `data/`, `security/`, `tests/`, `wizard/`, `report/`, `rng/`

---

## 7. Phased Roadmap

### Phase 1: Foundation (Week 1-2)

**Goal**: Build technical foundation skills + one domain prototype

| # | Task | Skill | Method |
|---|------|-------|--------|
| 1.1 | Init repo on GitHub, README, `.gitignore`, CI for skill validation | — | Manual |
| 1.2 | Build `odoo-v19-core` SKILL.md | odoo-v19-core | Hybrid |
| 1.3 | Build `odoo-v19-core` references/ | odoo-v19-core | AI-extract + review |
| 1.4 | Build `odoo-v19-views` SKILL.md + refs | odoo-v19-views | Hybrid |
| 1.5 | Build `odoo-v19-sale` SKILL.md + refs | odoo-v19-sale | Hybrid |
| 1.6 | Integration: add submodule + symlinks to a real project | all 3 | Manual |
| 1.7 | Verify discovery in both Claude Code and Antigravity | all 3 | Manual |
| 1.8 | Run real tasks, measure token savings vs. baseline | all 3 | Manual |

**Exit criteria**: 3 skills working in both agents, measurable token reduction on sale-related tasks.

### Phase 2: Core Domains (Week 3-4)

**Goal**: Cover the most-used business modules

| # | Task | Skill |
|---|------|-------|
| 2.1 | Build `odoo-v19-owl` | odoo-v19-owl |
| 2.2 | Build `odoo-v19-account` | odoo-v19-account |
| 2.3 | Build `odoo-v19-stock` | odoo-v19-stock |
| 2.4 | Build `odoo-v19-purchase` | odoo-v19-purchase |
| 2.5 | Build `odoo-v19-hr` | odoo-v19-hr |
| 2.6 | Refine Phase 1 skills based on real usage feedback | all |

**Exit criteria**: 8 skills total, covering the core Odoo ERP stack.

### Phase 3: Extended Domains (Week 5-6)

**Goal**: Cover remaining major modules

| # | Task | Skill |
|---|------|-------|
| 3.1 | Build `odoo-v19-mrp` | odoo-v19-mrp |
| 3.2 | Build `odoo-v19-project` | odoo-v19-project |
| 3.3 | Build `odoo-v19-crm` | odoo-v19-crm |
| 3.4 | Build `odoo-v19-website` | odoo-v19-website |
| 3.5 | Build `odoo-v19-pos` | odoo-v19-pos |
| 3.6 | Cross-module integration patterns (sale+stock, purchase+account, etc.) | references |

**Exit criteria**: 13 skills, full community coverage of major modules.

### Phase 4: Polish & Enterprise Prep (Week 7-8)

**Goal**: Harden, document, prepare for enterprise edition

| # | Task |
|---|------|
| 4.1 | Comprehensive real-world testing across team projects |
| 4.2 | Token savings benchmarking report |
| 4.3 | Contribution guide for team members to improve skills |
| 4.4 | Plan enterprise edition skill extensions |
| 4.5 | Publish v1.0 release |

---

## 8. Success Metrics

| Metric | Baseline (no skills) | Target (with skills) |
|--------|---------------------|----------------------|
| Tokens consumed per typical task | ~20-30K | ~5-8K |
| Time to first correct code output | ~60s (exploring) | ~15s (immediate) |
| Accuracy on first attempt | ~70% | ~90%+ |
| Need for human correction | Frequent | Rare |

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Skills become stale if Odoo updates | Wrong code generated | Version pin in metadata, review on Odoo upgrades |
| SKILL.md too large (>5K tokens) | Defeats token savings | Strict budget, move detail to references/ |
| Poor descriptions → skills not activated | No benefit | Test activation with diverse prompts |
| Over-detailed references → context bloat | Slow, expensive | Keep references focused, <3K tokens each |
| Team doesn't maintain skills | Decay over time | Contribution guide, PR review process |

---

## 10. Open Questions (To Resolve During Implementation)

1. **Code examples in skills?** Trade-off: more tokens vs. better output quality.
2. **Cross-module workflows?** (e.g., sale->stock->account chain) Separate skill or references in each?
3. **V19-specific changelog?** Should skills note what changed from v18->v19?
4. **Enterprise edition**: Separate skills or extend community skills with enterprise sections?

---

## 11. Key References

- Agent Skills specification: https://agentskills.io/specification
- What are skills: https://agentskills.io/what-are-skills
- Example skills by Anthropic: https://github.com/anthropics/skills
- Claude Code skills docs: https://code.claude.com/docs/en/skills
- Antigravity skills codelab: https://codelabs.developers.google.com/getting-started-with-antigravity-skills
- Skills placement guide (Antigravity): https://medium.com/google-cloud/confused-about-where-to-put-your-agent-skills-ea778f3c64f3
- Skills repo: https://github.com/kenghot-king/odoo19-agent-skills.git
- Roadmap: documents/roadmaps/odoo19-agent-skills.md

---

## 12. Next Steps

1. Create new project folder for `odoo19-agent-skills`
2. Init git repo and push to GitHub
3. Start Phase 1.2: Build `odoo-v19-core` SKILL.md by scanning Odoo v19 source
4. Copy this compact and the roadmap to the new project for context continuity

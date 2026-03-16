## Why

AI coding agents (Claude Code, Google Antigravity) spend ~20-30K tokens exploring the Odoo v19 codebase every session — reading `__manifest__.py`, model files, views, and framework internals — before writing any code. This wastes tokens, slows response time, and leads to ~70% first-attempt accuracy. Pre-built Agent Skills encoding Odoo v19 domain knowledge can cut token usage to ~5-8K, deliver immediate correct code output, and raise first-attempt accuracy to 90%+. Phase 1 establishes the foundation: the core framework skill and two proof-of-concept domain skills (views, sale) to validate the approach before scaling to all modules.

## What Changes

- Create `odoo-v19-core` skill: ORM, field types, model inheritance (`_inherit`, `_inherits`), `api.*` decorators, security (ACL + record rules), controllers, wizards, and module structure for Odoo 19 Community Edition
- Create `odoo-v19-views` skill: QWeb XML views (form, list, kanban, search), XPath inheritance patterns, actions, and menu definitions
- Create `odoo-v19-sale` skill: `sale.order` / `sale.order.line` models, quotation-to-invoice workflow, extension patterns, and common pitfalls
- Each skill includes a `SKILL.md` (< 5K tokens) with progressive disclosure to `references/*.md` files (< 3K tokens each) for detailed field lists, code patterns, and model schemas
- Skills follow the open [Agent Skills](https://agentskills.io) standard and work in both Claude Code (`.claude/skills/`) and Google Antigravity (`.agent/skills/`)

## Capabilities

### New Capabilities

- `odoo-v19-core-skill`: Core framework knowledge skill — ORM, fields, inheritance, security, controllers, wizards, module structure. SKILL.md + reference files for field-types, inheritance-patterns, security-acl, controllers-routes, and module-scaffold.
- `odoo-v19-views-skill`: View layer knowledge skill — form/list/kanban/search views, QWeb templating, XPath patterns, actions, menus. SKILL.md + reference files for each view type and XPath patterns.
- `odoo-v19-sale-skill`: Sale module domain skill — sale.order, sale.order.line, quotation workflow (draft → sent → sale → done/cancel), invoicing, delivery integration. SKILL.md + reference files for models, order-workflow, and invoicing.

### Modified Capabilities

(none — this is a greenfield project)

## Impact

- **New files**: 3 SKILL.md files + ~13 reference files across 3 skill directories
- **Source dependency**: Content is extracted from Odoo 19 Community source at `/Users/administrator/Developer/odoo_19/odoo/` — accuracy depends on reading actual model definitions, view XMLs, and framework code
- **Distribution**: Skills repo consumed as git submodule + symlinks in target Odoo projects
- **No runtime code changes**: Skills are static markdown documents, no code execution
- **Token budget constraint**: Each SKILL.md must stay under 5K tokens; each reference file under 3K tokens

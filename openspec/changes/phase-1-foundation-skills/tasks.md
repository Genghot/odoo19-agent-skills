## 1. Project Setup

- [x] 1.1 Create directory structure: `odoo-v19-core/`, `odoo-v19-core/references/`, `odoo-v19-views/`, `odoo-v19-views/references/`, `odoo-v19-sale/`, `odoo-v19-sale/references/`
- [x] 1.2 Initialize git repo, create `.gitignore`, and push to GitHub at `Genghot/odoo19-agent-skills`

## 2. Build odoo-v19-core Skill

- [x] 2.1 Read Odoo 19 ORM source (`odoo/orm/`, `odoo/models/`, `odoo/fields/`, `odoo/api/`) to extract field types, model classes, api decorators, and inheritance mechanisms
- [x] 2.2 Read `odoo/addons/base/` to extract security patterns (ir.model.access, ir.rule), controller patterns, and base model definitions
- [x] 2.3 Write `odoo-v19-core/SKILL.md` with frontmatter, Business Context, Key Models & Relations, Inheritance Patterns (3 types with examples), Security Patterns, Extension Patterns, Common Pitfalls (5+), and References links. Verify under 400 lines.
- [x] 2.4 Write `odoo-v19-core/references/field-types.md` — all field types with parameters. Verify under 250 lines.
- [x] 2.5 Write `odoo-v19-core/references/inheritance-patterns.md` — detailed examples of _inherit, _inherits, delegation. Verify under 250 lines.
- [x] 2.6 Write `odoo-v19-core/references/security-acl.md` — ACL CSV format, record rules XML, group definitions. Verify under 250 lines.
- [x] 2.7 Write `odoo-v19-core/references/controllers-routes.md` — HTTP controller class, route decorators, JSON-RPC patterns. Verify under 250 lines.
- [x] 2.8 Write `odoo-v19-core/references/module-scaffold.md` — complete module directory structure, __manifest__.py template, __init__.py patterns. Verify under 250 lines.

## 3. Build odoo-v19-views Skill

- [x] 3.1 Read Odoo 19 view source (`addons/web/`, `odoo/addons/base/`) and sample XML views from sale/stock/account to extract view patterns, XPath usage, action/menu definitions
- [x] 3.2 Write `odoo-v19-views/SKILL.md` with frontmatter, Business Context, Form View, List View, Kanban View, Search View, XPath Inheritance, Actions & Menus, Common Pitfalls (4+), and References links. Verify under 400 lines.
- [x] 3.3 Write `odoo-v19-views/references/form-view.md` — complete form elements, attributes, widgets. Verify under 250 lines.
- [x] 3.4 Write `odoo-v19-views/references/list-view.md` — list view attributes, editable modes, decorations. Verify under 250 lines.
- [x] 3.5 Write `odoo-v19-views/references/kanban-view.md` — kanban structure, QWeb template patterns, progressive web app cards. Verify under 250 lines.
- [x] 3.6 Write `odoo-v19-views/references/search-view.md` — search fields, filters, group-by, default filters via context. Verify under 250 lines.
- [x] 3.7 Write `odoo-v19-views/references/xpath-patterns.md` — comprehensive XPath examples for common extension scenarios (add field, move field, change attributes, replace element). Verify under 250 lines.

## 4. Build odoo-v19-sale Skill

- [x] 4.1 Read Odoo 19 sale module source (`addons/sale/models/*.py`) to extract sale.order and sale.order.line field definitions, state machine, key methods (action_confirm, _prepare_invoice_line, _compute_amounts)
- [x] 4.2 Read sale module views (`addons/sale/views/*.xml`) to extract view structure patterns and common XPath targets
- [x] 4.3 Read sale sub-modules (`sale_stock`, `sale_management`, `sale_project`, `sale_mrp`, `sale_purchase`) manifests to map the sub-module ecosystem
- [x] 4.4 Write `odoo-v19-sale/SKILL.md` with frontmatter, Business Context, Workflow (ASCII state diagram), Key Models (sale.order + sale.order.line with key fields), Amount Computation, Extension Patterns (_prepare_invoice_line, action_confirm hooks), Common Pitfalls (4+), Sub-module Map, and References links. Verify under 400 lines.
- [x] 4.5 Write `odoo-v19-sale/references/models.md` — complete field lists for sale.order and sale.order.line with types and descriptions. Verify under 250 lines.
- [x] 4.6 Write `odoo-v19-sale/references/order-workflow.md` — detailed state transitions, method signatures, hook points. Verify under 250 lines.
- [x] 4.7 Write `odoo-v19-sale/references/invoicing.md` — sale-to-invoice flow, _create_invoices, _prepare_invoice_line details. Verify under 250 lines.

## 5. Validation

- [x] 5.1 Verify all SKILL.md files have valid YAML frontmatter with name, description, and metadata fields
- [x] 5.2 Count tokens for each SKILL.md (must be < 5K) and each reference file (must be < 3K)
- [x] 5.3 Test skill description activation: for each skill, verify 5+ diverse prompts would match the description keywords
- [x] 5.4 Review all code examples against actual Odoo 19 source for accuracy
- [x] 5.5 Verify cross-references between skills are correct (e.g., sale → views, sale → account pointers)

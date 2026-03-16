# Phase 1 Skills Test Cases

> Copy-paste these prompts into a Claude Code session opened in `test_agent_skills/` to verify skills activate and produce correct Odoo 19 code.
>
> **Setup**: Skills are in `.claude/skills/odoo19-agent-skills/` (via symlink).
> Test modules go in `addons/`. Docker runs at localhost:8069 (CE) / :8070 (EE).

---

## Test 1: Core Skill — Create a new module from scratch

**Prompt**:
```
Create a new Odoo 19 module called "sale_discount_approval" in addons/.
It should add a Boolean field "requires_discount_approval" to res.company
and a Many2one field "discount_approver_id" (res.users) to res.company.
Include __manifest__.py, __init__.py, models/, security/, and views/.
```

**What to verify**:
- [ ] Agent uses correct module structure (not guessing)
- [ ] `__manifest__.py` has correct keys: name, version, depends, data, license
- [ ] `_inherit = 'res.company'` pattern used (not `_name`)
- [ ] `ir.model.access.csv` has correct column order
- [ ] Security XML loaded before views in manifest `data` list
- [ ] Fields use correct types and parameters

**Skill expected**: `odoo-v19-core` should activate (matches: module structure, ORM, fields, security, `_inherit`)

---

## Test 2: Views Skill — Create form and list views

**Prompt**:
```
Add a form view and list view for a new model "discount.request" with fields:
- sale_order_id (Many2one to sale.order)
- requested_by (Many2one to res.users)
- discount_percentage (Float)
- state (Selection: draft/pending/approved/rejected)
- notes (Text)

Include a statusbar, buttons for state transitions, and a search view with filters for "My Requests" and "Pending Approval". Add a menu item under the Sales root menu.
```

**What to verify**:
- [ ] Form uses `<form>` → `<header>` → `<sheet>` structure
- [ ] Statusbar: `<field name="state" widget="statusbar" statusbar_visible="...">`
- [ ] Buttons use `type="object"` with `invisible` as Python expression (not domain)
- [ ] List uses `<list>` tag (not `<tree>`)
- [ ] Search view has `<filter>` with `domain` and `name` attributes
- [ ] Action uses `ir.actions.act_window` with correct `view_mode`, `res_model`
- [ ] Menu uses `<menuitem>` with `parent` and `action`

**Skill expected**: `odoo-v19-views` + `odoo-v19-core` should activate

---

## Test 3: Sale Skill — Extend sale.order

**Prompt**:
```
Add a "discount_approval_status" Selection field (none/pending/approved/rejected)
to sale.order. Override action_confirm to check if any order line has discount > 10%,
and if so, set discount_approval_status to "pending" and prevent confirmation
until it's "approved". Add the field to the sale order form view.
```

**What to verify**:
- [ ] `_inherit = 'sale.order'` used correctly
- [ ] `action_confirm` override calls `super()` (pitfall #1)
- [ ] Uses `raise UserError(...)` to prevent confirmation, not silent return
- [ ] View extends `sale.view_order_form` via `inherit_id ref="sale.view_order_form"`
- [ ] XPath expression targets correct element in sale form
- [ ] `invisible`/`readonly` use Python expressions (v19 style)
- [ ] Field added to list view is `optional="show"` or `optional="hide"`

**Skill expected**: `odoo-v19-sale` + `odoo-v19-core` + `odoo-v19-views` should activate

---

## Test 4: Sale Skill — Customize invoice line

**Prompt**:
```
Add a "special_note" Char field to sale.order.line. When an invoice is created
from the sale order, pass this special_note to the invoice line.
```

**What to verify**:
- [ ] Adds field to `sale.order.line` via `_inherit`
- [ ] Also adds field to `account.move.line` via `_inherit`
- [ ] Overrides `_prepare_invoice_line` with `super()` call
- [ ] Returns dict with `special_note` added: `res['special_note'] = self.special_note`
- [ ] Extends both SO line form/list and invoice line views

**Skill expected**: `odoo-v19-sale` should activate (matches: `_prepare_invoice_line`, invoicing)

---

## Test 5: Core Skill — Security and access control

**Prompt**:
```
Create a security group "Discount Manager" in the sale_discount_approval module.
Regular sale users can read discount.request but only Discount Managers can
approve/reject. Add a record rule so users can only see their own requests
unless they are Discount Managers.
```

**What to verify**:
- [ ] Group XML uses `<record model="res.groups">` with `implied_ids`
- [ ] `ir.model.access.csv` has separate lines for user and manager groups
- [ ] Record rule uses `domain_force` with `[('requested_by', '=', user.id)]`
- [ ] Manager rule uses `[(1, '=', 1)]` to see all
- [ ] `noupdate="1"` on record rules
- [ ] Group referenced correctly in CSV as `module.group_xml_id`

**Skill expected**: `odoo-v19-core` should activate (matches: security, `ir.model.access`, `ir.rule`, groups)

---

## Test 6: Views Skill — Kanban view

**Prompt**:
```
Create a kanban view for discount.request grouped by state.
Show the sale order name, requested_by as avatar, discount_percentage,
and use color coding based on state.
```

**What to verify**:
- [ ] Uses `<kanban default_group_by="state">`
- [ ] Template uses `<t t-name="card">` (not `t-name="kanban-box"`)
- [ ] `many2one_avatar_user` widget for requested_by
- [ ] `<footer>` element used correctly
- [ ] Bootstrap utility classes for layout (d-flex, etc.)

**Skill expected**: `odoo-v19-views` should activate (matches: kanban view)

---

## Scoring

| # | Test | Skills Activated? | Code Correct? | No Codebase Exploration? |
|---|------|:-:|:-:|:-:|
| 1 | New module scaffold | | | |
| 2 | Form/list/search views | | | |
| 3 | Extend sale.order | | | |
| 4 | Customize invoice line | | | |
| 5 | Security & ACL | | | |
| 6 | Kanban view | | | |

**Pass criteria**:
- "Skills Activated?" = Agent uses skill knowledge, doesn't explore `addons/sale/` or `odoo/orm/`
- "Code Correct?" = Generated code follows v19 patterns (list not tree, Python expressions not domains for invisible, etc.)
- "No Codebase Exploration?" = Agent writes code immediately without reading Odoo source files

**Baseline comparison**: Run the same prompts WITHOUT skills (remove symlinks) and compare token usage + accuracy.

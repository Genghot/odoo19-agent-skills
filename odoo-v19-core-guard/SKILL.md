---
name: odoo-v19-core-guard
description: >
  Odoo 19 pitfalls for core framework. Breaking changes in ORM, fields,
  model inheritance (_inherit, _inherits), security (ir.model.access,
  ir.rule, res.groups), controllers, __manifest__.py, module structure.
  Use for any Odoo 19 development to avoid v19-specific install failures.
---

# Odoo 19 Core — Pitfalls & Breaking Changes

## Hard Failures

### `category_id` removed from `res.groups`
```xml
<!-- WRONG — crashes install -->
<field name="category_id" ref="base.module_category_sales"/>

<!-- CORRECT — just remove the line -->
<record id="group_foo" model="res.groups">
    <field name="name">Foo</field>
    <field name="implied_ids" eval="[(4, ref('other.group'))]"/>
</record>
```

### Model name collisions with existing Odoo models
Before using `_name = 'project.milestone'` or similar, verify the name isn't already taken by a standard Odoo module. Many common names are used:
`project.milestone`, `project.task.type`, `hr.leave.type`, `stock.rule`, etc.
Use a custom prefix: `_name = 'mymodule.milestone'`

## Wrong Patterns

### `name_get()` is deprecated — use `_compute_display_name`
```python
# WRONG — deprecated since v17
def name_get(self):
    return [(r.id, f"{r.name} [{r.code}]") for r in self]

# CORRECT
def _compute_display_name(self):
    for rec in self:
        rec.display_name = f"{rec.name} [{rec.code}]"
```

### Record rules must be wrapped in `noupdate="1"`
```xml
<!-- WRONG — rules get overwritten on module upgrade -->
<record id="rule_foo" model="ir.rule">...</record>

<!-- CORRECT -->
<data noupdate="1">
    <record id="rule_foo" model="ir.rule">
        <field name="name">Rule</field>
        <field name="model_id" ref="model_foo"/>
        <field name="domain_force">[('user_id', '=', user.id)]</field>
        <field name="groups" eval="[(4, ref('group_user'))]"/>
    </record>
</data>
```

## v19-Specific Syntax

- `ir.model.access.csv` column order: `id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink`
- `__manifest__.py` requires `license` key (e.g., `'LGPL-3'`)
- Security XML must load before views XML in manifest `data` list
- `@api.multi` was removed — do not use
- Use `self.env.user` not `self.env['res.users'].browse(uid)`

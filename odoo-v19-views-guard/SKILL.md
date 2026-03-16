---
name: odoo-v19-views-guard
description: >
  Odoo 19 pitfalls for views. Breaking changes in form, list, kanban,
  search views, XPath inheritance, settings views, actions, menus,
  invisible/readonly/required syntax. Use when creating or modifying
  Odoo 19 views to avoid deprecated patterns and install failures.
---

# Odoo 19 Views — Pitfalls & Breaking Changes

## Hard Failures

### Search view `<group>` does not support `expand` or `string`
```xml
<!-- WRONG — crashes install -->
<group expand="0" string="Group By">

<!-- CORRECT -->
<group>
    <filter name="group_state" string="State"
            context="{'group_by': 'state'}"/>
</group>
```

### View external IDs use `_tree` suffix, not `_list`
Despite `<list>` tag, external IDs keep `_tree`: `base.view_partner_tree`, `sale.view_order_tree`, etc.
```xml
<!-- WRONG -->
<field name="inherit_id" ref="base.view_partner_list"/>
<!-- CORRECT -->
<field name="inherit_id" ref="base.view_partner_tree"/>
```

### Settings view: `//app[@name='general']` XPath doesn't exist
```xml
<!-- WRONG — crashes install (no such element in v19 CE) -->
<xpath expr="//app[@name='general']" position="inside">

<!-- CORRECT — add a new app section inside the form -->
<xpath expr="//form" position="inside">
    <app data-string="My Settings" string="My Settings">
        <block title="My Feature">
            <setting string="Enable Feature" help="Description">
                <field name="my_boolean_field"/>
            </setting>
        </block>
    </app>
</xpath>
```

## Wrong Patterns

### `<tree>` is deprecated — use `<list>`
```xml
<!-- WRONG — works but deprecated -->
<tree string="Records">

<!-- CORRECT -->
<list string="Records">
```

### Kanban template: `t-name="card"` not `t-name="kanban-box"`
```xml
<!-- WRONG — old pattern -->
<t t-name="kanban-box">
    <div class="oe_kanban_card">

<!-- CORRECT — v19 pattern -->
<t t-name="card">
    <field name="name" class="fw-bold"/>
    <footer>
        <field name="user_id" widget="many2one_avatar_user"/>
    </footer>
```

## v19-Specific Syntax

- `invisible`/`readonly`/`required` use **Python expressions**: `invisible="state != 'draft'"` — NOT domain syntax
- List fields: `optional="show"` or `optional="hide"` for column toggle
- Form: `<form>` → `<header>` → `<sheet>` → `<chatter/>`
- Use `<list>` tag but external IDs still use `_tree` suffix (e.g., `sale.view_order_tree`)

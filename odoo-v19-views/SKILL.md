---
name: odoo-v19-views
description: >
  Odoo 19 view layer. QWeb XML views: form view, list view (formerly tree),
  kanban view, search view, calendar, pivot, graph, activity views. XPath
  view inheritance with position="after|before|inside|replace|attributes".
  ir.actions.act_window, ir.ui.menu, actions, menus, statusbar widget,
  field widgets, decorations. Use when creating or modifying Odoo views,
  menus, actions, or UI elements.
metadata:
  author: kenghot-king
  version: "1.0"
  odoo-version: "19.0"
  edition: community
---

# Odoo 19 Views

## Business Context

Odoo views are XML data files that define the UI. They live in the `views/` directory, are declared in `__manifest__.py` under `data`, and are stored as `ir.ui.view` records. Views are inherited and extended via XPath expressions. In Odoo 19, views use Python expression strings for `invisible`, `readonly`, and `required` attributes (not list-of-tuples domains).

## Form View

```xml
<record id="view_my_model_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <form string="My Model">
            <header>
                <button string="Confirm" name="action_confirm" type="object"
                        class="btn-primary" invisible="state != 'draft'"/>
                <field name="state" widget="statusbar"
                       statusbar_visible="draft,confirmed,done"/>
            </header>
            <sheet>
                <div class="oe_button_box" name="button_box">
                    <button name="action_view_invoices" type="object"
                            class="oe_stat_button" icon="fa-pencil-square-o"
                            invisible="invoice_count == 0">
                        <field name="invoice_count" widget="statinfo" string="Invoices"/>
                    </button>
                </div>
                <group name="main">
                    <group name="left">
                        <field name="partner_id"/>
                        <field name="date"/>
                    </group>
                    <group name="right">
                        <field name="user_id" widget="many2one_avatar_user"/>
                        <field name="company_id" groups="base.group_multi_company"/>
                    </group>
                </group>
                <notebook>
                    <page string="Lines" name="lines">
                        <field name="line_ids"/>
                    </page>
                    <page string="Notes" name="notes">
                        <field name="note"/>
                    </page>
                </notebook>
            </sheet>
            <chatter/>
        </form>
    </field>
</record>
```

**Key elements**: `<header>` (buttons + statusbar), `<sheet>` (content), `<group>` (field layout, 2 columns default), `<notebook>`/`<page>` (tabs), `<chatter/>` (mail.thread integration), `<div class="oe_button_box">` (stat buttons).

## List View

In Odoo 19, use `<list>` tag (not `<tree>`).

```xml
<record id="view_my_model_list" model="ir.ui.view">
    <field name="name">my.model.list</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <list string="My Models" multi_edit="1" sample="1"
              decoration-muted="state == 'cancel'"
              decoration-bf="state == 'confirmed'">
            <field name="name" decoration-bf="1"/>
            <field name="partner_id"/>
            <field name="date" optional="show"/>
            <field name="amount_total" sum="Total" widget="monetary"/>
            <field name="state" widget="badge"
                   decoration-success="state == 'done'"
                   decoration-info="state == 'draft'"/>
        </list>
    </field>
</record>
```

**Key attributes**: `multi_edit="1"` (bulk edit), `sample="1"` (sample data), `decoration-*` (conditional styling), `optional="show|hide"` (column visibility toggle), `column_invisible="True"` (always hidden), `sum="Label"` (footer aggregation).

**Decorations**: `decoration-bf` (bold), `decoration-muted`, `decoration-success` (green), `decoration-info` (blue), `decoration-warning` (orange), `decoration-danger` (red), `decoration-primary`.

## Kanban View

```xml
<record id="view_my_model_kanban" model="ir.ui.view">
    <field name="name">my.model.kanban</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <kanban default_group_by="stage_id" quick_create="true" sample="1">
            <progressbar field="activity_state"
                colors='{"planned": "success", "today": "warning", "overdue": "danger"}'/>
            <templates>
                <t t-name="card">
                    <field class="fw-bold fs-5" name="name"/>
                    <field name="partner_id" widget="many2one_avatar"/>
                    <field name="amount_total" widget="monetary"/>
                    <footer>
                        <field name="priority" widget="priority"/>
                        <field name="user_id" widget="many2one_avatar_user" class="ms-auto"/>
                    </footer>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

**Key attributes**: `default_group_by` (kanban columns), `quick_create` (inline card creation), `on_create="quick_create"`. Template uses `<t t-name="card">` with Bootstrap utility classes.

## Search View

```xml
<record id="view_my_model_search" model="ir.ui.view">
    <field name="name">my.model.search</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <search string="Search">
            <field name="name" filter_domain="['|', ('name', 'ilike', self), ('reference', 'ilike', self)]"/>
            <field name="partner_id" operator="child_of"/>
            <separator/>
            <filter string="My Records" name="my_records" domain="[('user_id', '=', uid)]"/>
            <filter string="This Month" name="this_month" date="create_date" default_period="this_month"/>
            <separator/>
            <group string="Group By">
                <filter string="Customer" name="customer" context="{'group_by': 'partner_id'}"/>
                <filter string="Date" name="date" context="{'group_by': 'date:month'}"/>
            </group>
        </search>
    </field>
</record>
```

**Key elements**: `<field>` (searchable fields, `filter_domain` for custom matching, `operator` for relational), `<filter>` (predefined filters with `domain`, date filters with `date` + `default_period`), `<group>` (group-by section with `context={'group_by': 'field'}`).

**Default filters via action context**: `{'search_default_my_records': 1}` activates the filter named `my_records`.

## XPath View Inheritance

```xml
<record id="view_my_model_form_inherit" model="ir.ui.view">
    <field name="name">my.model.form.inherit.my_module</field>
    <field name="model">my.model</field>
    <field name="inherit_id" ref="other_module.view_my_model_form"/>
    <field name="arch" type="xml">
        <!-- Add field after existing field -->
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="my_new_field"/>
        </xpath>

        <!-- Change field attributes -->
        <xpath expr="//field[@name='name']" position="attributes">
            <attribute name="readonly">state != 'draft'</attribute>
        </xpath>

        <!-- Add inside a group -->
        <xpath expr="//group[@name='left']" position="inside">
            <field name="custom_date"/>
        </xpath>

        <!-- Replace element entirely -->
        <xpath expr="//button[@name='old_action']" position="replace">
            <button string="New Action" name="new_action" type="object"/>
        </xpath>
    </field>
</record>
```

**Position values**: `after` (sibling after), `before` (sibling before), `inside` (first child), `replace` (swap element), `attributes` (modify attrs).

**XPath expressions**: `//field[@name='x']`, `//button[@name='x']`, `//group[@name='x']`, `//page[@name='x']`, `//notebook`, `//list`, `//div[hasclass('classname')]`.

## Actions & Menus

```xml
<!-- Window action -->
<record id="action_my_model" model="ir.actions.act_window">
    <field name="name">My Models</field>
    <field name="res_model">my.model</field>
    <field name="view_mode">list,kanban,form</field>
    <field name="domain">[('active', '=', True)]</field>
    <field name="context">{'search_default_my_records': 1, 'default_state': 'draft'}</field>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">Create your first record</p>
    </field>
</record>

<!-- Root menu -->
<menuitem id="menu_my_app_root" name="My App"
          web_icon="my_module,static/description/icon.png" sequence="25"/>
<!-- Sub-menu -->
<menuitem id="menu_my_model" name="My Models"
          parent="menu_my_app_root" action="action_my_model" sequence="10"/>
```

**Action key fields**: `res_model`, `view_mode` (comma-separated view types), `domain` (default filter), `context` (search defaults + creation defaults), `target` (`'current'`|`'new'`|`'inline_form'`), `search_view_id` (ref to search view).

## Common Pitfalls

1. **Using `<tree>` instead of `<list>`** — Odoo 19 uses `<list>` tag. `<tree>` still works but is deprecated.
2. **XPath not matching** — Common causes: field name typo, element doesn't exist in parent view, wrong parent element. Always verify the target exists.
3. **Forgetting `inherit_id`** — Without it, the view is standalone, not an extension. Must use `ref="module.view_id"`.
4. **`invisible`/`readonly`/`required` syntax** — In v19, these use Python expression strings: `invisible="state != 'draft'"`, NOT domain syntax `invisible="[('state', '!=', 'draft')]"`.
5. **Missing `name` attribute on `<group>`, `<page>`, `<div>`** — Without `name`, XPath targeting is fragile. Always add `name` for elements others may need to extend.
6. **Putting views before security in manifest** — Views referencing groups will fail if security XML isn't loaded first. Order: security → views → data.

## References

- `references/form-view.md` — Complete form elements, attributes, widgets
- `references/list-view.md` — List view attributes, editable modes, decorations
- `references/kanban-view.md` — Kanban structure, QWeb template patterns
- `references/search-view.md` — Search fields, filters, group-by, default activation
- `references/xpath-patterns.md` — Comprehensive XPath examples for extensions

# Odoo 19 Kanban View Reference

## Basic Structure

```xml
<kanban default_group_by="stage_id" quick_create="true" sample="1"
        on_create="quick_create" archivable="false">
    <field name="color"/>  <!-- declare fields used in templates -->
    <progressbar field="activity_state"
        colors='{"planned": "success", "today": "warning", "overdue": "danger"}'
        sum_field="expected_revenue"/>
    <templates>
        <t t-name="menu">
            <!-- Dropdown menu (optional) -->
            <a role="menuitem" type="edit" class="dropdown-item">Edit</a>
            <a role="menuitem" type="delete" class="dropdown-item">Delete</a>
            <field name="color" widget="kanban_color_picker"/>
        </t>
        <t t-name="card">
            <!-- Card content -->
            <field class="fw-bold fs-5" name="name"/>
            <field name="partner_id" widget="many2one_avatar"/>
            <field name="amount_total" widget="monetary"/>
            <field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
            <footer>
                <field name="priority" widget="priority" class="me-2"/>
                <field name="activity_ids" widget="kanban_activity"/>
                <field name="user_id" widget="many2one_avatar_user" class="ms-auto"/>
            </footer>
        </t>
    </templates>
</kanban>
```

## Kanban Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `default_group_by` | str | Field to group by (creates columns) |
| `quick_create` | `"true"` \| `"false"` | Enable inline card creation |
| `quick_create_view` | ref | Form view for quick create |
| `on_create` | `"quick_create"` | Action when clicking Create |
| `archivable` | `"true"` \| `"false"` | Allow archiving groups |
| `sample` | `"1"` | Show sample data when empty |
| `group_create` | `"true"` \| `"false"` | Allow creating new groups |
| `group_delete` | `"true"` \| `"false"` | Allow deleting groups |
| `group_edit` | `"true"` \| `"false"` | Allow editing group names |
| `records_draggable` | `"true"` \| `"false"` | Allow drag-and-drop |
| `highlight_color` | str | Field name for card left-border color |
| `js_class` | str | Custom JavaScript class |

## Progressbar

Shows progress within each column:

```xml
<progressbar field="kanban_state"
    colors='{"done": "success", "blocked": "danger", "normal": "muted"}'
    sum_field="expected_revenue"
    help="Revenue by Status"/>
```

- `field`: Selection field driving the progress segments
- `colors`: JSON mapping selection values to Bootstrap colors
- `sum_field`: Numeric field summed per group
- `help`: Tooltip text

## Templates

### Card Template (`t-name="card"`)

The main card layout. Uses Bootstrap utility classes directly.

```xml
<t t-name="card">
    <widget name="web_ribbon" title="Lost" bg_color="text-bg-danger"
            invisible="won_status != 'lost'"/>
    <field class="fw-bold fs-5" name="name"/>
    <div class="d-flex justify-content-between">
        <field name="partner_id" widget="many2one_avatar" readonly="1"/>
        <field name="expected_revenue" widget="monetary"/>
    </div>
    <footer class="pt-1">
        <field name="priority" widget="priority" class="me-2"/>
        <field name="user_id" widget="many2one_avatar_user" class="ms-auto"/>
    </footer>
</t>
```

**Common Bootstrap classes**: `d-flex`, `justify-content-between`, `fw-bold`, `fs-5`, `ms-auto`, `me-2`, `mt-auto`, `pt-1`, `o_text_block`, `o_text_bold`.

### Menu Template (`t-name="menu"`)

Optional dropdown menu for each card:

```xml
<t t-name="menu">
    <a role="menuitem" type="open" class="dropdown-item">Open</a>
    <a role="menuitem" type="edit" class="dropdown-item">Edit</a>
    <a role="menuitem" type="delete" class="dropdown-item">Delete</a>
    <ul class="oe_kanban_colorpicker"/>
    <field name="color" widget="kanban_color_picker"/>
</t>
```

Menu item `type` values: `open`, `edit`, `delete`, `set_cover`.

## QWeb Expressions in Kanban

```xml
<!-- Conditional rendering -->
<t t-if="record.state.raw_value == 'done'">
    <span class="badge text-bg-success">Done</span>
</t>

<!-- Field access in expressions -->
<t t-set="amount" t-value="record.expected_revenue.raw_value"/>
<span t-if="amount > 1000" class="text-success">High Value</span>

<!-- Check widget permissions -->
<t t-if="widget.editable">
    <a role="menuitem" type="edit">Edit</a>
</t>
```

**Available in templates**:
- `record.field_name.raw_value` — Raw field value
- `record.field_name.value` — Formatted display value
- `widget.editable` — Can user edit?
- `widget.deletable` — Can user delete?

## Kanban Widgets

| Widget | Description |
|--------|-------------|
| `many2one_avatar_user` | User avatar circle |
| `many2one_avatar` | Record avatar |
| `many2many_tags` | Colored tag pills |
| `priority` | Star rating |
| `kanban_activity` | Activity indicator |
| `kanban_color_picker` | Color selector in menu |
| `web_ribbon` | Corner ribbon badge |
| `monetary` | Currency amount |
| `remaining_days` | Days until deadline |

## Common Patterns

### Kanban with stages (CRM/Project style)

```xml
<kanban default_group_by="stage_id" on_create="quick_create"
        quick_create_view="module.quick_create_form_view">
```

### Kanban without grouping (grid of cards)

```xml
<kanban class="o_kanban_mobile">
    <!-- No default_group_by = ungrouped card grid -->
```

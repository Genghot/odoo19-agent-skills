# Odoo 19 Form View Reference

## Structure

```xml
<form string="Title" class="optional_css_class">
    <header><!-- buttons, statusbar --></header>
    <sheet>
        <div class="oe_button_box" name="button_box"><!-- stat buttons --></div>
        <widget name="web_ribbon" .../>  <!-- optional ribbon -->
        <div class="oe_title"><field name="name" placeholder="..."/></div>
        <group><!-- fields --></group>
        <notebook><page><!-- tabs --></page></notebook>
    </sheet>
    <chatter/>  <!-- mail.thread integration -->
</form>
```

## Top-Level Elements

| Element | Purpose |
|---------|---------|
| `<header>` | Action buttons and status bar at top |
| `<sheet>` | Main content area with padding |
| `<chatter/>` | Messages, activities, followers (requires mail.thread mixin) |

## Header Elements

### Buttons

```xml
<button string="Confirm" name="action_confirm" type="object"
        class="btn-primary" invisible="state != 'draft'"
        confirm="Are you sure?" data-hotkey="v" groups="base.group_user"/>
```

| Attribute | Description |
|-----------|-------------|
| `string` | Button label |
| `name` | Method name (`type="object"`) or action XML ID (`type="action"`) |
| `type` | `"object"` (call method) or `"action"` (trigger action) |
| `class` | `btn-primary`, `btn-secondary`, `oe_highlight` |
| `invisible` | Python expression to hide |
| `confirm` | Confirmation dialog text |
| `data-hotkey` | Keyboard shortcut letter |
| `groups` | Restrict to user groups |
| `context` | Extra context for the method call |

### Statusbar

```xml
<field name="state" widget="statusbar" statusbar_visible="draft,confirmed,done"/>
```

## Sheet Elements

### Field Groups

```xml
<group name="main" string="Optional Title">
    <group name="left">
        <field name="field_a"/>
        <field name="field_b"/>
    </group>
    <group name="right">
        <field name="field_c"/>
    </group>
</group>
```

- Outer `<group>` creates 2-column layout
- Inner `<group>` elements are columns
- Single `<group>` = fields stacked vertically with labels

### Notebook / Pages

```xml
<notebook>
    <page string="Details" name="details">
        <field name="line_ids"/>
    </page>
    <page string="Notes" name="notes" invisible="not note">
        <field name="note"/>
    </page>
</notebook>
```

### Stat Buttons

```xml
<div class="oe_button_box" name="button_box">
    <button name="action_view_invoices" type="object"
            class="oe_stat_button" icon="fa-pencil-square-o"
            invisible="invoice_count == 0">
        <field name="invoice_count" widget="statinfo" string="Invoices"/>
    </button>
</div>
```

### Ribbon

```xml
<widget name="web_ribbon" title="Archived" bg_color="text-bg-danger"
        invisible="active"/>
```

## Field Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Field name (required) |
| `widget` | str | Override default widget |
| `string` | str | Override label |
| `invisible` | expr | Python expression to hide |
| `readonly` | expr | Python expression for read-only |
| `required` | expr | Python expression for required |
| `domain` | domain | Filter for relational fields |
| `context` | dict | Extra context for relational fields |
| `options` | json | Widget-specific options |
| `placeholder` | str | Placeholder text |
| `nolabel` | "1" | Hide field label |
| `colspan` | int | Span multiple columns |
| `class` | str | CSS classes |
| `groups` | str | Restrict to user groups |

## Common Widgets

| Widget | Field Types | Description |
|--------|-------------|-------------|
| `statusbar` | Selection | Progress bar with clickable steps |
| `many2one_avatar_user` | Many2one | User avatar with dropdown |
| `many2one_avatar` | Many2one | Record avatar |
| `many2many_tags` | Many2many | Tag pills with optional colors |
| `many2many_checkboxes` | Many2many | Checkboxes instead of tags |
| `monetary` | Float/Monetary | Currency-formatted amount |
| `percentage` | Float | Percentage display |
| `statinfo` | Integer/Float | Stat button value |
| `boolean_toggle` | Boolean | Toggle switch |
| `boolean_favorite` | Boolean | Star icon |
| `priority` | Selection | Star rating |
| `image` | Binary | Image display/upload |
| `binary` | Binary | File upload/download |
| `html` | Html | Rich text editor |
| `date` | Date | Date picker |
| `daterange` | Date | Date range picker |
| `color` | Integer | Color picker |
| `handle` | Integer | Drag handle for reordering |
| `radio` | Selection | Radio buttons |
| `badge` | Selection | Colored badge |
| `remaining_days` | Date/Datetime | "X days left" display |
| `account-tax-totals-field` | Binary | Tax summary table |
| `analytic_distribution` | Json | Analytic distribution widget |
| `res_partner_many2one` | Many2one | Partner search with create |
| `many2one_barcode` | Many2one | Barcode scanner input |

## Inline List/Kanban in Form

For One2many fields:

```xml
<field name="order_line" widget="sol_o2m" mode="list,kanban"
       readonly="state == 'cancel' or locked">
    <list editable="bottom">
        <field name="product_id"/>
        <field name="product_uom_qty"/>
        <field name="price_unit"/>
        <field name="price_subtotal"/>
    </list>
</field>
```

- `mode="list,kanban"`: Available view modes
- `editable="bottom"` or `"top"`: Inline editing in list

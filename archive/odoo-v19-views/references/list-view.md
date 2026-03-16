# Odoo 19 List View Reference

## Basic Structure

```xml
<list string="Records" multi_edit="1" sample="1"
      decoration-muted="state == 'cancel'"
      decoration-bf="state == 'confirmed'"
      default_order="date desc, name">
    <header>
        <button string="Mass Action" name="%(module.action_id)d" type="action"/>
    </header>
    <field name="name" decoration-bf="1" readonly="1"/>
    <field name="partner_id"/>
    <field name="date" optional="show"/>
    <field name="amount" sum="Total" widget="monetary"/>
    <field name="state" widget="badge" optional="show"/>
</list>
```

**Note**: Odoo 19 uses `<list>` tag. `<tree>` is deprecated but still works.

## List Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `string` | str | View title |
| `editable` | `"top"` \| `"bottom"` | Enable inline editing (new rows at top/bottom) |
| `multi_edit` | `"1"` | Enable bulk editing of selected rows |
| `sample` | `"1"` | Show sample data when no records |
| `default_order` | str | Default sort (e.g., `"date desc, name"`) |
| `limit` | int | Records per page (default 80) |
| `groups_limit` | int | Groups per page when grouped |
| `expand` | `"1"` | Expand all groups by default |
| `open_form_view` | `"1"` | Always open form on click (not inline edit) |
| `js_class` | str | Custom JavaScript class |

## Field Attributes in List

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Field name |
| `string` | str | Column header override |
| `widget` | str | Widget override |
| `optional` | `"show"` \| `"hide"` | Column visibility default (user can toggle) |
| `column_invisible` | `"True"` | Always hidden (not toggleable) |
| `readonly` | expr | Python expression |
| `invisible` | expr | Python expression |
| `sum` | str | Footer sum label |
| `avg` | str | Footer average label |
| `decoration-*` | expr | Conditional cell styling |
| `nolabel` | `"1"` | Hide column header |
| `width` | str | Fixed column width (e.g., `"100px"`) |

## Decorations

Apply to `<list>` element (row-level) or `<field>` (cell-level):

```xml
<!-- Row decoration -->
<list decoration-danger="amount < 0" decoration-success="state == 'done'">

<!-- Cell decoration -->
<field name="amount" decoration-bf="1" decoration-danger="amount < 0"/>
```

| Decoration | Effect |
|------------|--------|
| `decoration-bf` | **Bold** text |
| `decoration-it` | *Italic* text |
| `decoration-muted` | Gray/muted text |
| `decoration-info` | Blue |
| `decoration-primary` | Primary color |
| `decoration-success` | Green |
| `decoration-warning` | Orange |
| `decoration-danger` | Red |

## Header Actions

Buttons in `<header>` appear above the list and act on selected records:

```xml
<header>
    <button string="Create Invoices"
            name="%(sale.action_view_sale_advance_payment_inv)d"
            type="action" class="btn-secondary"/>
    <button string="Confirm" name="action_confirm" type="object"/>
</header>
```

## Inline Editing

```xml
<list editable="bottom">
    <field name="product_id"/>
    <field name="quantity"/>
    <field name="price_unit"/>
    <field name="subtotal" readonly="1"/>  <!-- computed, read-only -->
</list>
```

- `editable="bottom"`: New rows added at bottom
- `editable="top"`: New rows added at top
- Click any row to edit inline
- Without `editable`, clicking opens the form view

## Grouping

List views support grouping via search view group-by filters or action context.

In the action context:
```xml
<field name="context">{'group_by': 'state'}</field>
```

## Sortable Columns

- Fields are sortable by default if `store=True`
- Disable sorting: handled at field level (non-stored computed fields can't be sorted)
- Custom drag ordering: `<field name="sequence" widget="handle"/>`

## Control Panel Buttons (Create, Import)

The list view automatically shows Create, Import, etc. based on ACLs. To disable:
```xml
<list create="0" edit="0" delete="0" import="0" export_xlsx="0">
```

## Common Patterns

### Colored badges for status

```xml
<field name="state" widget="badge"
       decoration-info="state == 'draft'"
       decoration-success="state == 'done'"
       decoration-warning="state == 'pending'"
       decoration-danger="state == 'cancel'"/>
```

### Activity widget

```xml
<field name="activity_ids" widget="list_activity" optional="show"/>
```

### Monetary with sum

```xml
<field name="amount_total" widget="monetary" sum="Total Tax Included"
       decoration-bf="1" optional="show"/>
```

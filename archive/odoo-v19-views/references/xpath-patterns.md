# Odoo 19 XPath Patterns Reference

## View Inheritance Setup

```xml
<record id="view_model_form_inherit_my_module" model="ir.ui.view">
    <field name="name">my.model.form.inherit.my_module</field>
    <field name="model">my.model</field>
    <field name="inherit_id" ref="other_module.view_model_form"/>
    <field name="arch" type="xml">
        <!-- XPath expressions here -->
    </field>
</record>
```

**Required**: `inherit_id` must reference the parent view via `ref="module.view_xml_id"`.

## Position Values

| Position | Effect |
|----------|--------|
| `after` | Insert as next sibling |
| `before` | Insert as previous sibling |
| `inside` | Insert as first child |
| `replace` | Replace the matched element |
| `attributes` | Modify element attributes |

## Common XPath Patterns

### Add a field after another field

```xml
<xpath expr="//field[@name='partner_id']" position="after">
    <field name="my_custom_field"/>
</xpath>
```

### Add a field before another field

```xml
<xpath expr="//field[@name='date_order']" position="before">
    <field name="priority" widget="priority"/>
</xpath>
```

### Add field inside a named group

```xml
<xpath expr="//group[@name='sale_header']" position="inside">
    <field name="warehouse_id"/>
</xpath>
```

### Add a new page to notebook

```xml
<xpath expr="//notebook" position="inside">
    <page string="Custom Info" name="custom_info">
        <group>
            <field name="custom_field_1"/>
            <field name="custom_field_2"/>
        </group>
    </page>
</xpath>
```

### Add a stat button

```xml
<xpath expr="//div[@name='button_box']" position="inside">
    <button name="action_view_deliveries" type="object"
            class="oe_stat_button" icon="fa-truck"
            invisible="delivery_count == 0">
        <field name="delivery_count" widget="statinfo" string="Deliveries"/>
    </button>
</xpath>
```

### Add button to header

```xml
<xpath expr="//header" position="inside">
    <button string="Generate Report" name="action_generate_report"
            type="object" invisible="state != 'sale'"/>
</xpath>
```

### Modify field attributes

```xml
<xpath expr="//field[@name='partner_id']" position="attributes">
    <attribute name="readonly">state != 'draft'</attribute>
    <attribute name="required">True</attribute>
    <attribute name="domain">[('is_company', '=', True)]</attribute>
</xpath>
```

### Make a field invisible

```xml
<xpath expr="//field[@name='old_field']" position="attributes">
    <attribute name="invisible">True</attribute>
</xpath>
```

### Replace an element entirely

```xml
<xpath expr="//button[@name='action_old']" position="replace">
    <button string="New Action" name="action_new" type="object"
            class="btn-primary"/>
</xpath>
```

### Remove an element (replace with nothing)

```xml
<xpath expr="//field[@name='obsolete_field']" position="replace"/>
```

### Add field to list view

```xml
<xpath expr="//field[@name='amount_total']" position="before">
    <field name="discount_total" widget="monetary" optional="hide"/>
</xpath>
```

### Add column to inline list (One2many)

```xml
<xpath expr="//field[@name='order_line']/list/field[@name='price_unit']" position="after">
    <field name="margin" widget="monetary"/>
</xpath>
```

### Extend search view

```xml
<xpath expr="//filter[@name='my_records']" position="after">
    <filter string="High Priority" name="high_priority"
            domain="[('priority', '=', '1')]"/>
</xpath>
```

### Add group-by to search view

```xml
<xpath expr="//group" position="inside">
    <filter string="Category" name="group_category"
            context="{'group_by': 'category_id'}"/>
</xpath>
```

## XPath Expression Syntax

### By attribute

```xml
expr="//field[@name='partner_id']"
expr="//button[@name='action_confirm']"
expr="//filter[@name='draft']"
expr="//group[@name='main']"
expr="//page[@name='details']"
```

### By tag

```xml
expr="//notebook"
expr="//header"
expr="//sheet"
expr="//list"
expr="//form"
expr="//chatter"
```

### By CSS class

```xml
expr="//div[hasclass('oe_button_box')]"
expr="//div[hasclass('oe_title')]"
```

### Nested paths

```xml
expr="//notebook/page[@name='lines']"
expr="//field[@name='order_line']/list"
expr="//group[@name='main']/group[@name='left']"
```

### Multiple conditions

```xml
expr="//field[@name='state'][@widget='statusbar']"
```

## Prioritization

When multiple inherited views modify the same parent:

```xml
<field name="priority" eval="20"/>  <!-- Higher = applied later (overrides lower) -->
```

Default priority is 16. Use higher values to ensure your changes apply after others.

## Common Mistakes

1. **XPath doesn't match**: Field was renamed or moved in a newer version. Always check the parent view.
2. **Missing `inherit_id`**: View becomes standalone instead of inheriting.
3. **Wrong module in ref**: `ref="wrong_module.view_id"` — must match the module that defines the parent view.
4. **Ambiguous XPath**: `//field[@name='name']` may match multiple elements. Use more specific paths: `//group[@name='left']/field[@name='name']`.
5. **Position="inside" on field**: Fields don't have children. Use `after` or `before` instead.

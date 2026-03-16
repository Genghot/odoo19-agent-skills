# Odoo 19 Search View Reference

## Basic Structure

```xml
<search string="Search Records">
    <!-- Searchable fields -->
    <field name="name"/>
    <field name="partner_id" operator="child_of"/>

    <separator/>

    <!-- Predefined filters -->
    <filter string="My Records" name="my_records"
            domain="[('user_id', '=', uid)]"/>
    <filter string="Archived" name="archived"
            domain="[('active', '=', False)]"/>

    <separator/>

    <!-- Date filters -->
    <filter string="Created This Month" name="this_month"
            date="create_date" default_period="this_month"/>

    <separator/>

    <!-- Group-by -->
    <group string="Group By">
        <filter string="Customer" name="group_customer"
                context="{'group_by': 'partner_id'}"/>
        <filter string="Date" name="group_date"
                context="{'group_by': 'create_date:month'}"/>
    </group>
</search>
```

## Field Element

Adds a field to the search bar autocomplete:

```xml
<field name="name"/>
<field name="partner_id" operator="child_of"/>
<field name="description" string="Description"
       filter_domain="['|', ('name', 'ilike', self), ('description', 'ilike', self)]"/>
```

| Attribute | Description |
|-----------|-------------|
| `name` | Field name |
| `string` | Override label in search dropdown |
| `operator` | Search operator: `=`, `!=`, `>`, `<`, `>=`, `<=`, `ilike`, `like`, `child_of` |
| `filter_domain` | Custom domain. Use `self` as placeholder for user input |
| `groups` | Restrict to user groups |
| `invisible` | Hide from search |

### Multi-field search

```xml
<field name="name" string="Order"
       filter_domain="['|', '|',
           ('name', 'ilike', self),
           ('client_order_ref', 'ilike', self),
           ('partner_id.name', 'ilike', self)]"/>
```

## Filter Element

Predefined domain filters:

```xml
<filter string="Draft" name="draft" domain="[('state', '=', 'draft')]"/>
<filter string="High Value" name="high_value" domain="[('amount', '>', 10000)]"/>
<filter string="Active" name="active" domain="[('active', '=', True)]"
        help="Show only active records"/>
```

| Attribute | Description |
|-----------|-------------|
| `string` | Display label |
| `name` | Unique identifier (used for `search_default_*`) |
| `domain` | Odoo domain expression |
| `help` | Tooltip text |
| `invisible` | Hide filter |
| `groups` | Restrict to groups |

### Date filters

```xml
<filter string="Order Date" name="date_order" date="date_order"/>
<filter string="Created" name="created" date="create_date" default_period="this_month"/>
```

| Attribute | Description |
|-----------|-------------|
| `date` | Date/Datetime field name |
| `default_period` | `"this_month"`, `"this_quarter"`, `"this_year"`, `"last_7_days"`, `"last_30_days"`, `"last_365_days"` |

Date filters auto-generate period selector (day/week/month/quarter/year).

### Multiple filters = OR within group, AND between groups

```xml
<!-- These are OR'd (within same visual group) -->
<filter string="Draft" name="draft" domain="[('state', '=', 'draft')]"/>
<filter string="Sent" name="sent" domain="[('state', '=', 'sent')]"/>
<separator/>
<!-- These are AND'd with the above group -->
<filter string="My Records" name="mine" domain="[('user_id', '=', uid)]"/>
```

## Group-By Filters

```xml
<group string="Group By">
    <filter string="Customer" name="group_customer"
            context="{'group_by': 'partner_id'}"/>
    <filter string="Status" name="group_state"
            context="{'group_by': 'state'}"/>
    <filter string="Month" name="group_month"
            context="{'group_by': 'date_order:month'}"/>
</group>
```

Date grouping intervals: `day`, `week`, `month`, `quarter`, `year`.

## Default Filters via Action Context

Activate filters by default when opening the action:

```xml
<record id="action_my_model" model="ir.actions.act_window">
    <field name="context">{
        'search_default_my_records': 1,
        'search_default_draft': 1,
        'search_default_group_customer': 1,
    }</field>
</record>
```

Pattern: `search_default_{filter_name}: 1`

For fields (auto-search on value):
```xml
<field name="context">{'search_default_partner_id': active_id}</field>
```

## Domain Syntax Quick Reference

```python
# Simple conditions
[('state', '=', 'draft')]
[('amount', '>', 100)]
[('name', 'ilike', 'test')]     # case-insensitive contains
[('name', '=like', 'test%')]    # SQL LIKE pattern

# Operators: =, !=, >, >=, <, <=, like, ilike, =like, =ilike,
#            in, not in, child_of, parent_of

# Boolean operators
['|', ('state', '=', 'draft'), ('state', '=', 'sent')]   # OR
['&', ('state', '=', 'sale'), ('amount', '>', 100)]       # AND (implicit default)
['!', ('active', '=', True)]                               # NOT

# Special variables in search views
uid           # current user ID
today         # current date string
self          # user's search input (in filter_domain)
company_ids   # user's allowed company IDs
company_id    # current company ID
```

## Separator

```xml
<separator/>                        <!-- Horizontal separator between filter groups -->
<separator orientation="vertical"/> <!-- Vertical separator within a group -->
```

Filters between separators are OR'd. Filters across separators are AND'd.

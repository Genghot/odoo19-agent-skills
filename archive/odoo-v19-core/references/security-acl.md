# Odoo 19 Security Reference

## User Groups

Groups define permission levels. Declared in XML:

```xml
<odoo>
    <!-- Category (optional, for grouping in Settings) -->
    <record id="module_category_my_app" model="ir.module.category">
        <field name="name">My App</field>
        <field name="sequence">10</field>
    </record>

    <!-- User group -->
    <record id="group_my_app_user" model="res.groups">
        <field name="name">User</field>
        <field name="category_id" ref="module_category_my_app"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>

    <!-- Manager group (inherits User permissions) -->
    <record id="group_my_app_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="category_id" ref="module_category_my_app"/>
        <field name="implied_ids" eval="[(4, ref('group_my_app_user'))]"/>
        <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
    </record>
</odoo>
```

**Key fields**:
- `implied_ids`: Groups whose permissions this group inherits (use `(4, ref(...))` to link)
- `users`: Pre-assign users to this group
- `category_id`: Groups displayed together in Settings

**Built-in groups** (from `base`):
- `base.group_user` — Internal User (Employee)
- `base.group_system` — Settings (Administrator)
- `base.group_no_one` — Technical Features (debug mode)
- `base.group_public` — Public User
- `base.group_portal` — Portal User
- `base.group_multi_company` — Multi-company

## Access Control Lists (ir.model.access.csv)

File: `security/ir.model.access.csv`

**Format**:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

**Example**:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,my_module.group_my_app_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,my_module.group_my_app_manager,1,1,1,1
access_my_model_portal,my.model.portal,model_my_model,base.group_portal,1,0,0,0
```

**Column rules**:
- `id`: Unique XML ID (convention: `access_{model}_{group}`)
- `model_id:id`: `model_` + model `_name` with dots replaced by underscores (e.g., `sale.order` → `model_sale_order`)
- `group_id:id`: Full XML ID of the group (`module.group_name`). Leave empty for global access (all users).
- Permissions: `1` = granted, `0` = denied

**Important**: This file must be listed in `__manifest__.py` under `data`:
```python
'data': [
    'security/security.xml',        # groups first
    'security/ir.model.access.csv', # then ACLs
],
```

## Record Rules (ir.rule)

File: `security/ir_rules.xml` or `security/security.xml`

Record rules filter which records a user can access. They apply on top of ACLs.

### Multi-company rule (most common)

```xml
<odoo noupdate="1">
    <record id="my_model_company_rule" model="ir.rule">
        <field name="name">My Model: multi-company</field>
        <field name="model_id" ref="model_my_model"/>
        <field name="domain_force">[('company_id', 'in', company_ids)]</field>
    </record>
</odoo>
```

### Per-user rule

```xml
<record id="my_model_personal_rule" model="ir.rule">
    <field name="name">My Model: own records only</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="groups" eval="[(4, ref('my_module.group_my_app_user'))]"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>
```

### Manager override (see all records)

```xml
<record id="my_model_manager_rule" model="ir.rule">
    <field name="name">My Model: manager sees all</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="groups" eval="[(4, ref('my_module.group_my_app_manager'))]"/>
    <field name="domain_force">[(1, '=', 1)]</field>
</record>
```

### Rule behavior

- `noupdate="1"`: Rule won't be overwritten on module upgrade (important for customized rules)
- **No groups specified**: Rule is global (applies to all users, AND-combined with other rules)
- **Groups specified**: Rule applies only to those groups (OR-combined within same model for same group)
- `domain_force` variables: `user` (current user browse record), `company_ids` (user's company IDs), `company_id` (current company ID), `time` (Python time module)

## Field-Level Access

Restrict field visibility to specific groups:

```python
secret_field = fields.Char(groups='base.group_system')
salary = fields.Monetary(groups='hr.group_hr_user')
```

Fields with `groups` are:
- Hidden in views for users outside those groups
- Protected from read/write via ORM for unauthorized users

## Common Security Patterns

### Sudo (bypass security)

```python
# Execute with superuser privileges
self.sudo().write({'state': 'confirmed'})

# Read bypassing record rules
record = self.env['sale.order'].sudo().browse(order_id)

# CAUTION: sudo() bypasses both ACLs and record rules
# Always validate business logic before using sudo
```

### Check access programmatically

```python
# Check if user has group
if self.env.user.has_group('sale.group_sale_manager'):
    ...

# Check model-level access
self.env['sale.order'].check_access('write')

# Check record-level access
record.check_access('read')
```

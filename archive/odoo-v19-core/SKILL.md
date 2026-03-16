---
name: odoo-v19-core
description: >
  Odoo 19 core framework. ORM, field types (Char, Integer, Float, Boolean, Date,
  Datetime, Selection, Many2one, One2many, Many2many, Html, Binary, Monetary,
  Reference, Image, Json, Properties), model inheritance (_inherit, _inherits),
  api decorators (depends, onchange, constrains, model, model_create_multi,
  autovacuum, readonly), security (ir.model.access, ir.rule), controllers,
  wizards (TransientModel), __manifest__.py, and module structure. Use for any
  Odoo 19 development task.
metadata:
  author: kenghot-king
  version: "1.0"
  odoo-version: "19.0"
  edition: community
---

# Odoo 19 Core Framework

## Business Context

This skill covers the Odoo 19 core framework used by every module: the ORM (Object-Relational Mapping), field system, model inheritance mechanisms, security layer (access control lists and record rules), web controllers, and transient model wizards. Activate this skill for any Odoo 19 development task.

## Key Model Classes

```
BaseModel (metaclass=MetaModel)
├── AbstractModel   (_abstract=True, no DB table)
│   └── Model       (_auto=True, creates DB table)
│       └── TransientModel  (_transient=True, auto-vacuumed)
```

- **Model**: Regular persistent models. Use for business objects (sale.order, res.partner, etc.)
- **TransientModel**: Temporary data for wizards. Auto-cleaned. Simplified ACL (users see only their own records).
- **AbstractModel**: Mixins and base classes. No DB table. Use for shared behavior (mail.thread, portal.mixin).

## Field Types (Summary)

| Category | Types |
|----------|-------|
| **Scalar** | `Char`, `Text`, `Html`, `Integer`, `Float`, `Monetary`, `Boolean`, `Date`, `Datetime`, `Selection`, `Binary`, `Image`, `Json` |
| **Relational** | `Many2one`, `One2many`, `Many2many`, `Reference`, `Many2oneReference` |
| **Special** | `Properties`, `PropertiesDefinition`, `Id` |

**Common parameters** (all fields): `string`, `help`, `readonly`, `required`, `index`, `default`, `groups`, `company_dependent`, `copy`, `store`, `compute`, `precompute`, `inverse`, `search`, `related`, `aggregator`, `translate`

See `references/field-types.md` for full parameter details per field type.

## API Decorators

| Decorator | Purpose | Example |
|-----------|---------|---------|
| `@api.depends('field1', 'field2.sub')` | Declare compute dependencies | Triggers recomputation on change |
| `@api.depends_context('company')` | Context-dependent compute | Non-stored fields varying by context |
| `@api.constrains('field1')` | Validation on write | Raise `ValidationError` if invalid |
| `@api.onchange('field1')` | Form-only UI reaction | Return `{'warning': {...}}` |
| `@api.model` | Method on model, not records | `self` is empty recordset |
| `@api.model_create_multi` | Create accepting list of vals | Standard `create()` pattern in v19 |
| `@api.ondelete(at_uninstall=False)` | Prevent deletion conditionally | Raise error if record shouldn't be deleted |
| `@api.autovacuum` | Daily cron cleanup | For TransientModel garbage collection |
| `@api.readonly` | Read-only DB cursor via RPC | For reporting/read endpoints |

## Inheritance Patterns

### 1. Classical Inheritance (extend existing model)

```python
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_points = fields.Integer(string="Loyalty Points", default=0)

    def action_reset_points(self):
        self.write({'loyalty_points': 0})
```

- No `_name` needed (same model, same table)
- Adds columns to existing table
- Can override methods (always call `super()`)

### 2. Prototype Inheritance (new model from parent)

```python
class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Sales Order"
```

- `_name` + `_inherit` = new model inheriting fields/methods from parents
- Creates its own DB table
- Multiple parents allowed (mixin pattern)

### 3. Delegation Inheritance (_inherits)

```python
class ProductProduct(models.Model):
    _name = 'product.product'
    _inherits = {'product.template': 'product_tmpl_id'}

    product_tmpl_id = fields.Many2one('product.template', required=True, ondelete='cascade')
```

- Transparent field access: `product.name` reads from `product.template`
- Only FK stored on child table; data lives on parent
- Many2one field must be `required=True`, `ondelete='cascade'` or `'restrict'`

## Security

### Access Control Lists (ir.model.access.csv)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,my_module.group_manager,1,1,1,1
```

Columns: `id` (XML ID), `name` (display), `model_id:id` (use `model_` + model name with dots→underscores), `group_id:id` (group XML ID), permissions (1/0).

### Record Rules (ir.rule)

```xml
<odoo noupdate="1">
    <record id="my_model_company_rule" model="ir.rule">
        <field name="name">My Model: multi-company</field>
        <field name="model_id" ref="model_my_model"/>
        <field name="domain_force">[('company_id', 'in', company_ids)]</field>
        <field name="perm_read" eval="True"/>
        <field name="perm_write" eval="True"/>
        <field name="perm_create" eval="True"/>
        <field name="perm_unlink" eval="True"/>
    </record>
</odoo>
```

## Extension Patterns

- **Add fields**: `_inherit = 'model.name'` + field declarations
- **Override methods**: Redefine method, call `super()` first or last depending on logic
- **Extend views**: Use XPath inheritance (see `odoo-v19-views` skill)
- **Add menu items**: Define `ir.actions.act_window` + `ir.ui.menu` in XML

### Method override pattern

```python
def action_confirm(self):
    # Pre-processing
    for order in self:
        if not order.custom_field:
            raise UserError(_("Custom field is required."))
    res = super().action_confirm()
    # Post-processing
    self._do_custom_logic()
    return res
```

## Common Pitfalls

1. **Forgetting `super()` in overrides** — breaks downstream logic (e.g., skipping `super().action_confirm()` prevents stock picking creation in `sale_stock`)
2. **Missing `store=True` on computed fields** — without it, field can't be used in `search()`, `group_by`, or SQL queries. Add `store=True` if you need DB-level access.
3. **Using `@api.onchange` for stored logic** — onchange only runs in form UI, not on programmatic writes. Use `compute` with `store=True` for persistent derived values.
4. **Wrong CSV column order in ir.model.access.csv** — must be exactly: id, name, model_id:id, group_id:id, perm_read, perm_write, perm_create, perm_unlink
5. **Forgetting `__init__.py` imports** — new model files must be imported in `models/__init__.py` and `models/` must be imported in the module's root `__init__.py`
6. **Using `@api.depends` with non-stored related fields** — triggers won't fire. Spell out the full dependency path: `@api.depends('order_id.partner_id.name')` not `@api.depends('partner_name')` if `partner_name` is `related`
7. **Not adding fields to `__manifest__.py`** — new data/view XML files must be listed in the `data` key or they won't load

## Module Structure

```
my_module/
├── __init__.py              # imports models/, controllers/, wizard/
├── __manifest__.py          # metadata, depends, data files
├── models/
│   ├── __init__.py          # imports each model file
│   └── my_model.py
├── views/
│   └── my_model_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml         # groups, record rules
├── data/                    # default data, sequences, crons
├── static/                  # web assets (JS, CSS, images)
├── controllers/             # HTTP endpoints
├── wizard/                  # TransientModel + views
├── report/                  # QWeb report templates
├── tests/                   # Python test cases
└── i18n/                    # translations
```

See `references/module-scaffold.md` for `__manifest__.py` template and `__init__.py` patterns.

## References

- `references/field-types.md` — All field types with constructor parameters
- `references/inheritance-patterns.md` — Detailed inheritance examples
- `references/security-acl.md` — ACL, record rules, and group definitions
- `references/controllers-routes.md` — HTTP controllers and route decorators
- `references/module-scaffold.md` — Module directory structure and manifest template

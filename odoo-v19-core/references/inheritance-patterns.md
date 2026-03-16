# Odoo 19 Inheritance Patterns Reference

## Pattern 1: Classical Inheritance (Extend Existing Model)

The most common pattern. Adds fields/methods to an existing model without creating a new one.

```python
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    # No _name — extends the existing res.partner

    loyalty_points = fields.Integer(string="Loyalty Points", default=0)
    loyalty_level = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ], string="Loyalty Level", compute='_compute_loyalty_level', store=True)

    @api.depends('loyalty_points')
    def _compute_loyalty_level(self):
        for partner in self:
            if partner.loyalty_points >= 1000:
                partner.loyalty_level = 'gold'
            elif partner.loyalty_points >= 500:
                partner.loyalty_level = 'silver'
            else:
                partner.loyalty_level = 'bronze'

    def action_reset_points(self):
        self.write({'loyalty_points': 0})
```

**Effect**: Adds `loyalty_points` and `loyalty_level` columns to the existing `res_partner` table.

### Method Override with super()

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # Pre-processing: validate before confirmation
        for order in self:
            if order.amount_total <= 0:
                raise UserError(_("Cannot confirm order with zero amount."))
        # Call parent implementation
        res = super().action_confirm()
        # Post-processing: custom logic after confirmation
        self._send_custom_notification()
        return res
```

### Overriding create/write

```python
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'custom_field' not in vals:
                vals['custom_field'] = 'default_value'
        return super().create(vals_list)

    def write(self, vals):
        if 'price_unit' in vals:
            # Log price changes
            for line in self:
                line.message_post(body=f"Price changed from {line.price_unit} to {vals['price_unit']}")
        return super().write(vals)
```

## Pattern 2: Prototype Inheritance (New Model from Parents)

Creates a new model that inherits fields and methods from one or more parent models.

```python
class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = "Sales Order"
    _order = 'date_order desc, id desc'

    name = fields.Char(string="Order Reference", required=True, index='trigram')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sale', 'Sales Order'),
    ], default='draft')
```

**Effect**: Creates a new `sale_order` table with all fields from portal.mixin, mail.thread, mail.activity.mixin, utm.mixin, plus its own fields.

### Multi-mixin pattern

```python
class MyModel(models.Model):
    _name = 'my.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "My Model"

    # Gets message_ids, activity_ids, etc. from mixins
    name = fields.Char(required=True)
```

## Pattern 3: Delegation Inheritance (_inherits)

Composition pattern — child model delegates field access to parent via a Many2one FK.

```python
class ProductProduct(models.Model):
    _name = 'product.product'
    _inherits = {'product.template': 'product_tmpl_id'}
    _description = "Product Variant"

    product_tmpl_id = fields.Many2one(
        'product.template', string="Product Template",
        required=True, ondelete='cascade',
    )
    barcode = fields.Char(string="Barcode")  # own field on product_product table
    # product.name, product.list_price, etc. transparently read from product.template
```

**Effect**:
- `product_product` table has only `product_tmpl_id` FK + variant-specific fields
- Accessing `product.name` transparently reads `product.product_tmpl_id.name`
- Creating a product.product auto-creates a product.template if not provided

### Rules for _inherits

- The Many2one field **must** have `required=True`
- `ondelete` should be `'cascade'` or `'restrict'`
- Multiple delegation is possible: `_inherits = {'model.a': 'a_id', 'model.b': 'b_id'}`
- Fields from parent are read/write transparent — no need for `related`

## Comparison Table

| Aspect | Classical (`_inherit`) | Prototype (`_name` + `_inherit`) | Delegation (`_inherits`) |
|--------|----------------------|--------------------------------|------------------------|
| New table? | No | Yes | Yes |
| New model? | No | Yes | Yes |
| Shares parent data? | Yes (same table) | No (copies structure) | Yes (via FK) |
| Use case | Extend existing model | New model with mixin behavior | Composition / variant pattern |
| Example | Add field to res.partner | sale.order inheriting mail.thread | product.product → product.template |

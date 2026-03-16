from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    discount_reason = fields.Char(string='Discount Reason')

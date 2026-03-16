from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    internal_note = fields.Text(string='Internal Note')

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    priority = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('urgent', 'Urgent'),
            ('critical', 'Critical'),
        ],
        string='Priority',
        default='normal',
        required=True,
    )
    priority_note = fields.Text(string='Priority Note')

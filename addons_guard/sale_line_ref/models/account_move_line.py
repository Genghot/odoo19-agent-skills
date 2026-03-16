from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_ref = fields.Char(string='Customer Reference')

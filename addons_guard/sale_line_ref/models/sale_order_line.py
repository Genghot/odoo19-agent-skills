from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_ref = fields.Char(string='Customer Reference')

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['customer_ref'] = self.customer_ref
        return res

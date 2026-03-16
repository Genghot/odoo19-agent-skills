from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_by = fields.Many2one(
        comodel_name='res.users',
        string='Confirmed By',
        readonly=True,
        copy=False,
    )

    def action_confirm(self):
        for order in self:
            order.confirmed_by = self.env.user
            if (
                order.amount_total > 10000
                and not self.env.user.has_group('sales_team.group_sale_manager')
            ):
                raise UserError(
                    "Only Sales Managers can confirm orders exceeding 10,000."
                )
        return super().action_confirm()

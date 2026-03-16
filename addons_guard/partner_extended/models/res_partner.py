from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    loyalty_level = fields.Selection(
        selection=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
        ],
        string='Loyalty Level',
    )
    loyalty_points = fields.Integer(string='Loyalty Points', default=0)
    loyalty_display = fields.Char(
        string='Loyalty Display',
        compute='_compute_loyalty_display',
    )

    @api.depends('loyalty_level', 'loyalty_points')
    def _compute_loyalty_display(self):
        for record in self:
            if record.loyalty_level:
                level_label = dict(
                    record._fields['loyalty_level'].selection
                ).get(record.loyalty_level, '')
                record.loyalty_display = f"Level: {level_label} ({record.loyalty_points} points)"
            else:
                record.loyalty_display = False

    @api.depends('name', 'loyalty_level')
    def _compute_display_name(self):
        super()._compute_display_name()
        for record in self:
            if record.loyalty_level and record.display_name:
                level_label = dict(
                    record._fields['loyalty_level'].selection
                ).get(record.loyalty_level, '')
                record.display_name = f"{record.display_name} [{level_label}]"

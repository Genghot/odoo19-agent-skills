from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_serial_tracking = fields.Boolean(
        related='company_id.use_serial_tracking',
        readonly=False,
        string='Use Serial Tracking',
    )
    default_equipment_status = fields.Selection(
        related='company_id.default_equipment_status',
        readonly=False,
        string='Default Equipment Status',
    )

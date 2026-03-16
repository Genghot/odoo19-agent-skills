from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    use_serial_tracking = fields.Boolean(
        string='Use Serial Tracking',
        default=False,
    )
    default_equipment_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('retired', 'Retired'),
    ], string='Default Equipment Status', default='active')

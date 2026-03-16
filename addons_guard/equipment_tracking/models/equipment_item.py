from odoo import api, fields, models


class EquipmentItem(models.Model):
    _name = 'equipment.item'
    _description = 'Equipment Item'

    name = fields.Char(string='Name', required=True)
    serial_number = fields.Char(string='Serial Number')
    purchase_date = fields.Date(string='Purchase Date')
    status = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('in_use', 'In Use'),
            ('maintenance', 'Maintenance'),
            ('retired', 'Retired'),
        ],
        string='Status',
        default='available',
        required=True,
    )
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    notes = fields.Html(string='Notes')

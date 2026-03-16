from odoo import api, fields, models


class HelpdeskAssignWizard(models.TransientModel):
    _name = 'helpdesk.assign.wizard'
    _description = 'Helpdesk Mass Assign Wizard'

    user_id = fields.Many2one('res.users', string='Assign To', required=True)
    ticket_ids = fields.Many2many(
        'helpdesk.ticket',
        string='Tickets',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'ticket_ids' in fields_list:
            active_ids = self.env.context.get('active_ids', [])
            res['ticket_ids'] = [(6, 0, active_ids)]
        return res

    def action_assign(self):
        self.ensure_one()
        self.ticket_ids.write({'assigned_to': self.user_id.id})
        return {'type': 'ir.actions.act_window_close'}

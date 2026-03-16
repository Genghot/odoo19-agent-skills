from odoo import api, fields, models


class ProjectCustomMilestone(models.Model):
    _name = 'project.custom.milestone'
    _description = 'Project Milestone'
    _order = 'deadline asc, id'

    name = fields.Char(string='Name', required=True)
    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade')
    deadline = fields.Date(string='Deadline')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True, tracking=True)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    description = fields.Html(string='Description')
    progress = fields.Float(string='Progress (%)')

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name or ''

    def action_start(self):
        self.ensure_one()
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancelled'

    def action_reset_draft(self):
        self.ensure_one()
        self.state = 'draft'

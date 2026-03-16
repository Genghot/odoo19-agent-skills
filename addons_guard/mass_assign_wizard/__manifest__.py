{
    'name': 'Mass Assign Wizard',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Mass assign helpdesk tickets to a user',
    'depends': ['helpdesk_lite'],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_assign_wizard_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}

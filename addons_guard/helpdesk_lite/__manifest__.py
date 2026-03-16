{
    'name': 'Helpdesk Lite',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Lightweight helpdesk ticket management',
    'depends': ['base'],
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_ticket_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

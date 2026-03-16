{
    'name': 'Ticket Search',
    'version': '19.0.1.0.0',
    'category': 'Helpdesk',
    'summary': 'Enhanced search view for helpdesk tickets',
    'description': 'Adds advanced search filters and group-by options for helpdesk tickets.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['helpdesk_lite'],
    'data': [
        'views/helpdesk_ticket_search.xml',
    ],
    'installable': True,
    'application': False,
}

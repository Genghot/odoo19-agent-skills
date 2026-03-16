{
    'name': 'Sale Line Reference',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Customer reference field on sale and invoice lines',
    'description': 'Adds a customer reference field to sale order lines that propagates to invoice lines.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
}

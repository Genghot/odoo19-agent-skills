{
    'name': 'Sale Priority',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add priority level to sale orders',
    'description': 'Adds priority and priority note fields to sale orders with list decorations.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}

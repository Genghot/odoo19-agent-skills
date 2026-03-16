{
    'name': 'Sale Confirm Check',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Validation checks on sale order confirmation',
    'description': 'Tracks who confirmed the order and enforces amount limits for non-managers.',
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

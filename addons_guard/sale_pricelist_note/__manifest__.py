{
    'name': 'Sale Pricelist Note',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Internal notes on pricelists and discount reasons on items',
    'description': 'Adds internal note to pricelists and discount reason to pricelist items.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_pricelist_views.xml',
    ],
    'installable': True,
    'application': False,
}

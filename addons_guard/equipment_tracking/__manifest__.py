{
    'name': 'Equipment Tracking',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Track equipment items, serial numbers, and assignments',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/equipment_item_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

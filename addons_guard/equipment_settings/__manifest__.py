{
    'name': 'Equipment Settings',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Configuration settings for equipment tracking',
    'description': 'Adds serial tracking and default status settings for equipment.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['equipment_tracking'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
}

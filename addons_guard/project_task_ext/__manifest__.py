{
    'name': 'Project Task Extension',
    'version': '19.0.1.0.0',
    'category': 'Project',
    'summary': 'Custom milestones for projects',
    'description': 'Adds a custom milestone model to the project module.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_custom_milestone_views.xml',
    ],
    'installable': True,
    'application': False,
}

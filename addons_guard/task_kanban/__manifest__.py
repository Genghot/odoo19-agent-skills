{
    'name': 'Task Kanban',
    'version': '19.0.1.0.0',
    'category': 'Project',
    'summary': 'Kanban view for project custom milestones',
    'description': 'Adds a kanban view for the project custom milestone model.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['project_task_ext'],
    'data': [
        'views/project_custom_milestone_kanban.xml',
    ],
    'installable': True,
    'application': False,
}

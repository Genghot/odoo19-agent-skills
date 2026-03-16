{
    'name': 'Sale Custom Report',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom terms and payment details in sale order report',
    'description': 'Extends the sale order report to show terms, conditions and payment term details.',
    'author': 'Genghot',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'report/sale_report_templates.xml',
    ],
    'installable': True,
    'application': False,
}

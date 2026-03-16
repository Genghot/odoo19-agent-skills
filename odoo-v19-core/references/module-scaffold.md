# Odoo 19 Module Scaffold Reference

## Directory Structure

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   ├── my_model_views.xml
│   └── menu.xml
├── security/
│   ├── security.xml          # groups, record rules
│   └── ir.model.access.csv   # ACLs
├── data/
│   └── data.xml              # default data, sequences, crons
├── demo/
│   └── demo.xml              # demo data (only loaded with demo flag)
├── static/
│   ├── description/
│   │   └── icon.png          # module icon (128x128)
│   └── src/
│       ├── js/               # OWL components, JS
│       ├── scss/             # stylesheets
│       └── xml/              # QWeb templates for JS
├── controllers/
│   ├── __init__.py
│   └── main.py
├── wizard/
│   ├── __init__.py
│   ├── my_wizard.py
│   └── my_wizard_views.xml
├── report/
│   ├── my_report.xml         # QWeb report template
│   └── my_report_views.xml   # report action
├── tests/
│   ├── __init__.py
│   └── test_my_model.py
└── i18n/
    └── my_module.pot          # translation template
```

## __manifest__.py Template

```python
{
    'name': 'My Module',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Short description for module list',
    'description': """
Long description of what the module does.
    """,
    'author': 'Your Name',
    'website': 'https://example.com',
    'license': 'LGPL-3',
    'depends': [
        'sale',       # list all module dependencies
    ],
    'data': [
        # Load order matters! Security first, then views, then data.
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/my_model_views.xml',
        'views/menu.xml',
        'data/data.xml',
        'wizard/my_wizard_views.xml',
        'report/my_report.xml',
        'report/my_report_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/scss/**/*',
            'my_module/static/src/js/**/*',
            'my_module/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    # 'post_init_hook': '_post_init_hook',
    # 'uninstall_hook': '_uninstall_hook',
}
```

### Manifest key reference

| Key | Type | Description |
|-----|------|-------------|
| `name` | str | Module display name |
| `version` | str | `odoo_version.module_version` (e.g., `19.0.1.0.0`) |
| `category` | str | Slash-separated category path |
| `summary` | str | One-line summary |
| `description` | str | Detailed description |
| `author` | str | Author name(s) |
| `license` | str | `'LGPL-3'`, `'GPL-3'`, `'OEEL-1'`, `'OPL-1'` |
| `depends` | list | Required module names |
| `data` | list | Data/view XML files (loaded in order) |
| `demo` | list | Demo data files |
| `assets` | dict | Web assets by bundle |
| `installable` | bool | Can be installed (default True) |
| `auto_install` | bool/list | Auto-install when deps met |
| `application` | bool | Show in Apps menu |
| `post_init_hook` | str | Function called after install |
| `uninstall_hook` | str | Function called before uninstall |
| `external_dependencies` | dict | `{'python': ['lib'], 'bin': ['cmd']}` |

## __init__.py Patterns

### Module root __init__.py

```python
from . import models
from . import controllers
from . import wizard


def _post_init_hook(env):
    """Called after module installation."""
    env['my.model'].search([]).write({'active': True})
```

### models/__init__.py

```python
from . import my_model
from . import my_other_model
```

**Important**: Every `.py` file in `models/` must be imported here or its models won't be registered.

## Wizard (TransientModel) Example

```python
# wizard/my_wizard.py
from odoo import fields, models

class MyWizard(models.TransientModel):
    _name = 'my.module.wizard'
    _description = "My Wizard"

    date_from = fields.Date(required=True, default=fields.Date.today)
    partner_id = fields.Many2one('res.partner', string="Customer")

    def action_apply(self):
        # self.env.context.get('active_ids') has the records that launched the wizard
        active_ids = self.env.context.get('active_ids', [])
        records = self.env['sale.order'].browse(active_ids)
        records.write({'partner_id': self.partner_id.id})
        return {'type': 'ir.actions.act_window_close'}
```

```xml
<!-- wizard/my_wizard_views.xml -->
<odoo>
    <record id="my_wizard_form" model="ir.ui.view">
        <field name="name">my.module.wizard.form</field>
        <field name="model">my.module.wizard</field>
        <field name="arch" type="xml">
            <form string="My Wizard">
                <group>
                    <field name="date_from"/>
                    <field name="partner_id"/>
                </group>
                <footer>
                    <button string="Apply" name="action_apply" type="object" class="btn-primary"/>
                    <button string="Cancel" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <record id="action_my_wizard" model="ir.actions.act_window">
        <field name="name">My Wizard</field>
        <field name="res_model">my.module.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
        <field name="binding_model_id" ref="sale.model_sale_order"/>
        <field name="binding_view_types">list,form</field>
    </record>
</odoo>
```

## Cron Job Example

```xml
<!-- data/data.xml -->
<odoo noupdate="1">
    <record id="ir_cron_my_task" model="ir.cron">
        <field name="name">My Module: Daily Task</field>
        <field name="model_id" ref="model_my_model"/>
        <field name="state">code</field>
        <field name="code">model._cron_daily_task()</field>
        <field name="interval_number">1</field>
        <field name="interval_type">days</field>
        <field name="numbercall">-1</field>
    </record>
</odoo>
```

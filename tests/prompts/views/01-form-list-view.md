# Test: Form and List Views

## Prompt

```
Create a new Odoo 19 module called "project_task_ext" in addons/.
It has a new model "project.milestone" with fields:
- name (Char, required)
- project_id (Many2one to project.project) — NOTE: depends on 'project'
- deadline (Date)
- state (Selection: draft/in_progress/done/cancelled, default='draft')
- responsible_id (Many2one to res.users)
- description (Html)
- progress (Float, widget=progressbar)

Create a form view with statusbar, state transition buttons, and a list view.
Add a menu item under the Project root menu.
```

## Verify

- [ ] Form uses `<form>` → `<header>` → `<sheet>` structure
- [ ] Statusbar: `<field name="state" widget="statusbar" statusbar_visible="...">`
- [ ] Buttons use `type="object"` with `invisible` as Python expression (NOT domain)
- [ ] List uses `<list>` tag (NOT `<tree>`)
- [ ] Action uses `ir.actions.act_window` with `view_mode` and `res_model`
- [ ] Menu uses `<menuitem>` with `parent` and `action`
- [ ] Module installs in Docker without errors

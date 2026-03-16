# Test: Wizard / Transient Model

## Prompt

```
Create a new Odoo 19 module called "mass_assign_wizard" in addons/.
It depends on the module "helpdesk_lite".
It should have a wizard (transient model) "helpdesk.assign.wizard" that:
1. Has a Many2one field "user_id" (res.users) for the assignee
2. Has a Many2many field "ticket_ids" (helpdesk.ticket) for selected tickets
3. Has an action_assign method that sets assigned_to on all selected tickets
4. Opens from a button in the helpdesk ticket list view via a server action
```

## Verify

- [ ] Wizard model inherits from `models.TransientModel`
- [ ] `_name = 'helpdesk.assign.wizard'`
- [ ] Has `_description` on the transient model
- [ ] Wizard has proper access rights in `ir.model.access.csv`
- [ ] Action uses `target='new'` for dialog window
- [ ] View uses `<footer>` for wizard buttons (not `<header>`)
- [ ] `ticket_ids` default populated from active_ids context
- [ ] Module installs in Docker without errors

# Test: Security Groups and ACL

## Prompt

```
Create a new Odoo 19 module called "helpdesk_lite" in addons/.
It should have:
1. A new model "helpdesk.ticket" with fields: name, description (Text),
   assigned_to (Many2one res.users), priority (Selection: low/medium/high/urgent),
   state (Selection: new/in_progress/resolved/closed)
2. Two security groups: "Helpdesk User" and "Helpdesk Manager"
3. Users can read/create tickets, Managers get full CRUD
4. A record rule so users only see tickets assigned to them,
   but Managers see all tickets
```

## Verify

- [ ] Group XML uses `<record model="res.groups">`
- [ ] Groups do NOT use `category_id` field (removed in v19)
- [ ] Manager group uses `implied_ids` to include user group
- [ ] `ir.model.access.csv` has separate lines for user and manager groups
- [ ] Record rule uses `domain_force` with correct syntax
- [ ] Record rule wrapped in `<data noupdate="1">`
- [ ] Manager rule uses `[(1, '=', 1)]` for full access
- [ ] Group referenced in CSV as `module.group_xml_id`
- [ ] Module installs in Docker without errors

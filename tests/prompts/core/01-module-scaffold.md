# Test: Module Scaffold

## Prompt

```
Create a new Odoo 19 module called "equipment_tracking" in addons/.
It should have a new model "equipment.item" with fields:
- name (Char, required)
- serial_number (Char)
- purchase_date (Date)
- status (Selection: available/in_use/maintenance/retired, default='available')
- assigned_to (Many2one to res.users)
- notes (Html)

Include __manifest__.py, __init__.py, models/, security/, and a basic form+list view.
```

## Verify

- [ ] `__manifest__.py` has keys: name, version, depends, data, license
- [ ] `version` follows `19.0.x.x.x` format
- [ ] `depends` includes `['base']`
- [ ] `license` is `LGPL-3`
- [ ] Security CSV loaded before views in `data` list
- [ ] `ir.model.access.csv` has correct column order: id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
- [ ] Model uses `_name = 'equipment.item'` and `_description`
- [ ] Fields use correct types and parameters
- [ ] Module installs in Docker without errors

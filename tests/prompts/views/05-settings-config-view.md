# Test: Settings / Config View

## Prompt

```
Create a new Odoo 19 module called "equipment_settings" in addons/.
It should:
1. Add a Boolean field "use_serial_tracking" to res.config.settings
   (related to a field on res.company)
2. Add a Selection field "default_equipment_status" to res.config.settings
   (related to res.company)
3. Display these settings in the General Settings page under a new
   "Equipment Tracking" section
This module depends on "equipment_tracking".
```

## Verify

- [ ] Settings model inherits `res.config.settings` via `_inherit`
- [ ] Fields use `related='company_id.field_name'` pattern
- [ ] Company model extended with the actual stored fields
- [ ] View inherits the correct settings form view
- [ ] XPath targets a valid element in the settings form (NOT `//app[@name='general']` which doesn't exist in v19 CE without base_setup)
- [ ] Uses `<setting>` and `<block>` elements for the settings UI
- [ ] Module installs in Docker without errors

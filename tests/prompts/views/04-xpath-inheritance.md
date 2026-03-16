# Test: XPath View Inheritance

## Prompt

```
Create a new Odoo 19 module called "partner_view_ext" in addons/.
It should modify the res.partner form view:
1. Add a "loyalty_level" field after the "email" field
2. Add a "loyalty_points" field after "loyalty_level"
3. Make "loyalty_points" readonly when loyalty_level is 'platinum'
4. Add a new notebook page "Loyalty Info" with a text note field
5. Add "loyalty_level" to the partner list view with optional="show"
This module depends on "partner_extended".
```

## Verify

- [ ] Inherits `base.view_partner_form` via `inherit_id ref="base.view_partner_form"`
- [ ] XPath expressions target correct elements: `//field[@name='email']`
- [ ] `readonly` uses Python expression: `readonly="loyalty_level == 'platinum'"` (NOT domain)
- [ ] `<page>` element has `name` attribute for future extensibility
- [ ] List view inherits correct parent view
- [ ] `optional="show"` used on list field
- [ ] Module installs in Docker without errors

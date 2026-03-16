# Test: Model Inheritance

## Prompt

```
Create a new Odoo 19 module called "partner_extended" in addons/.
It should:
1. Add a "loyalty_level" Selection field (bronze/silver/gold/platinum) to res.partner
2. Add a "loyalty_points" Integer field to res.partner
3. Add a computed field "loyalty_display" that shows "Level: X (Y points)"
4. Override the name_get method to append the loyalty level in brackets
```

## Verify

- [ ] Uses `_inherit = 'res.partner'` (not `_name`)
- [ ] No `_description` on inherited model (only on new models)
- [ ] Computed field has `@api.depends` with correct dependencies
- [ ] `name_get` override calls `super()`
- [ ] Selection field has proper tuples format
- [ ] Module installs in Docker without errors

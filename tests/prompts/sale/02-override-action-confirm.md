# Test: Override action_confirm

## Prompt

```
Create a new Odoo 19 module called "sale_confirm_check" in addons/.
It should:
1. Add a "confirmed_by" Many2one field (res.users) to sale.order
2. Override action_confirm to:
   - Set confirmed_by to the current user
   - Check if the order total exceeds 10000, and if so, require that the
     user belongs to the "Sales Manager" group; otherwise raise UserError
   - Call super() to proceed with normal confirmation
3. Add confirmed_by to the sale order form view (readonly)
```

## Verify

- [ ] `_inherit = 'sale.order'` used correctly
- [ ] `action_confirm` override calls `super()` (critical pitfall)
- [ ] Uses `raise UserError(...)` to prevent confirmation (not silent return)
- [ ] Uses `self.env.user.has_group('sales_team.group_sale_manager')` for group check
- [ ] `confirmed_by` field is readonly in view using Python expression
- [ ] Module installs in Docker without errors

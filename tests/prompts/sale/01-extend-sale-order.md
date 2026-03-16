# Test: Extend sale.order

## Prompt

```
Create a new Odoo 19 module called "sale_priority" in addons/.
It should:
1. Add a "priority" Selection field (normal/urgent/critical) to sale.order
2. Add a "priority_note" Text field to sale.order
3. Add both fields to the sale order form view after the partner_shipping_id field
4. Add "priority" to the sale order list view with optional="show"
5. Add a color decoration on the list: red for critical, orange for urgent
```

## Verify

- [ ] Uses `_inherit = 'sale.order'`
- [ ] View inherits `sale.view_order_form` via `inherit_id ref="sale.view_order_form"`
- [ ] XPath expression targets a valid element in sale form
- [ ] `invisible`/`readonly` use Python expressions (v19 style)
- [ ] List view uses `decoration-danger` and `decoration-warning` with Python expressions
- [ ] `optional="show"` on list field
- [ ] Module installs in Docker without errors

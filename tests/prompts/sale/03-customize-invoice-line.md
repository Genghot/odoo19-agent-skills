# Test: Customize Invoice Line

## Prompt

```
Create a new Odoo 19 module called "sale_line_ref" in addons/.
It should:
1. Add a "customer_ref" Char field to sale.order.line
2. Add a "customer_ref" Char field to account.move.line
3. When creating an invoice from the sale order, pass customer_ref
   from the SO line to the invoice line
4. Show customer_ref in the SO line list (inside the form) and invoice line list
```

## Verify

- [ ] Adds field to `sale.order.line` via `_inherit`
- [ ] Adds field to `account.move.line` via `_inherit`
- [ ] Overrides `_prepare_invoice_line` with `super()` call
- [ ] Returns dict with `customer_ref` added: `res['customer_ref'] = self.customer_ref`
- [ ] Extends SO form's line list and invoice form's line list views
- [ ] Module installs in Docker without errors

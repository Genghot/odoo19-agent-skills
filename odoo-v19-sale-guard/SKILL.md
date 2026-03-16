---
name: odoo-v19-sale-guard
description: >
  Odoo 19 pitfalls for sale module. Breaking changes in sale.order,
  sale.order.line, action_confirm, _prepare_invoice_line, quotation
  workflow, pricelist. Use when extending sales, quotations, or
  invoicing from sales to avoid common mistakes.
---

# Odoo 19 Sale — Pitfalls & Breaking Changes

## Hard Failures

### View external IDs use `_tree` suffix, not `_list`
```xml
<!-- WRONG -->
<field name="inherit_id" ref="sale.view_order_list"/>

<!-- CORRECT -->
<field name="inherit_id" ref="sale.view_order_tree"/>
```
Same for quotation view: `sale.view_quotation_tree`

## Wrong Patterns

### Always call `super()` in `action_confirm` override
```python
# WRONG — breaks stock picking, invoicing, and all other hooks
def action_confirm(self):
    # custom logic...
    return True

# CORRECT
def action_confirm(self):
    for order in self:
        # pre-confirmation checks
        if some_condition:
            raise UserError(_("Cannot confirm: reason"))
    res = super().action_confirm()
    # post-confirmation logic
    return res
```

### `_prepare_invoice_line` must call `super()` and return dict
```python
# WRONG — loses all standard invoice line values
def _prepare_invoice_line(self, **optional_values):
    return {'custom_field': self.custom_field}

# CORRECT
def _prepare_invoice_line(self, **optional_values):
    res = super()._prepare_invoice_line(**optional_values)
    res['custom_field'] = self.custom_field
    return res
```

### Don't modify `amount_total` directly
`amount_total`, `amount_untaxed`, `amount_tax` are stored computed fields.
Modify line-level values (qty, price_unit, discount, tax_ids) — totals recompute automatically.

### Filter out display_type lines
SO lines can be sections/notes with no product:
```python
for line in order.order_line:
    if line.display_type:
        continue  # skip section/note lines
    # process real lines
```

## v19-Specific Syntax

- `sale.order` states: `draft`, `sent`, `sale`, `cancel`
- Use `raise UserError(...)` to block confirmation — not silent `return`
- `action_confirm()` returns a value — always `return super().action_confirm()`
- Invoice line field: add to both `sale.order.line` AND `account.move.line`
- XPath targets in sale form: `//field[@name='payment_term_id']`, `//group[@name='sale_header']`, `//field[@name='partner_shipping_id']`

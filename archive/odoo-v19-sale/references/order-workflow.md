# Odoo 19 Sale Order Workflow Reference

## State Machine

```
SALE_ORDER_STATE = [
    ('draft', "Quotation"),
    ('sent', "Quotation Sent"),
    ('sale', "Sales Order"),
    ('cancel', "Cancelled"),
]
```

**Note**: There is no explicit `'done'` state in v19. Instead, `locked=True` on a `'sale'` order prevents modifications.

## Transition Methods

### action_draft()

**Signature**: `def action_draft(self)`
**From states**: `cancel`, `sent`
**To state**: `draft`
**Logic**:
- Filters to orders with state in `['cancel', 'sent']`
- Sets `state = 'draft'`
- Sets `locked = False`

### action_quotation_sent()

**Signature**: `def action_quotation_sent(self)`
**From state**: `draft`
**To state**: `sent`
**Logic**:
- Filters to orders with state `'draft'`
- Sets `state = 'sent'`

### action_confirm()

**Signature**: `def action_confirm(self)`
**From states**: `draft`, `sent`
**To state**: `sale`
**Logic** (simplified):
1. Validates orders (checks for invoiceable lines, etc.)
2. Sets `date_order` if not already set
3. Sets `state = 'sale'`
4. Triggers `_action_confirm()` for post-confirmation logic
5. Sends confirmation email if configured

**Hook points**:
- Override `action_confirm()` for pre/post confirmation logic
- Override `_action_confirm()` for internal post-confirmation
- `sale_stock` hooks here to create `stock.picking`
- `sale_project` hooks here to create tasks/projects

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # Pre-confirmation validation
        for order in self:
            if order.amount_total <= 0:
                raise UserError(_("Cannot confirm a zero-amount order."))
        res = super().action_confirm()
        # Post-confirmation logic
        self._do_something_after_confirm()
        return res
```

### action_cancel()

**Signature**: `def action_cancel(self)`
**From states**: `draft`, `sent`, `sale`
**To state**: `cancel`
**Logic**:
- Cancels related draft invoices
- Sets `state = 'cancel'`

### action_lock() / action_unlock()

**Signatures**: `def action_lock(self)` / `def action_unlock(self)`
**Logic**:
- `action_lock()`: Sets `locked = True`
- `action_unlock()`: Sets `locked = False`

## Invoice Status Computation

```python
INVOICE_STATUS = [
    ('upselling', 'Upselling Opportunity'),
    ('invoiced', 'Fully Invoiced'),
    ('to invoice', 'To Invoice'),
    ('no', 'Nothing to Invoice'),
]
```

**Computed via `_compute_invoice_status()`**:
- `'no'`: No lines with qty_to_invoice > 0
- `'to invoice'`: Lines have qty_to_invoice > 0
- `'invoiced'`: All delivered qty is invoiced
- `'upselling'`: Delivered qty exceeds ordered qty

## Line-Level Invoice Quantity Logic

### qty_invoiced

Depends on: `invoice_lines.move_id.state`, `invoice_lines.quantity`
- Sums `quantity` from linked invoice lines where move is NOT cancelled
- For credit notes (`out_refund`): subtracts quantity

### qty_to_invoice

Depends on: `qty_invoiced`, `qty_delivered`, `product_uom_qty`, `state`
- **Invoice policy = 'order'**: `qty_to_invoice = product_uom_qty - qty_invoiced`
- **Invoice policy = 'delivery'**: `qty_to_invoice = qty_delivered - qty_invoiced`
- Only computed when state is `'sale'` or `'done'`

### qty_delivered

Depends on: `qty_delivered_method`, `analytic_line_ids`
- **method = 'manual'**: Set by user
- **method = 'analytic'**: Sums from analytic lines
- **sale_stock** overrides this to compute from stock moves
- **sale_project** overrides for timesheet-based delivery

## Key Computed Fields Dependency Chain

```
product_id change
  └─► _compute_name (description)
  └─► _compute_product_uom_id (UoM)
  └─► _compute_tax_ids (taxes)
  └─► _compute_price_unit (unit price from pricelist)
  └─► _compute_discount (discount from pricelist)

price_unit / discount / product_uom_qty / tax_ids change
  └─► _compute_amount (price_subtotal, price_tax, price_total)
      └─► _compute_amounts on sale.order (amount_untaxed, amount_tax, amount_total)

partner_id change on sale.order
  └─► _compute_partner_invoice_id
  └─► _compute_partner_shipping_id
  └─► _compute_pricelist_id
  └─► _compute_fiscal_position_id
  └─► _compute_payment_term_id
```

## Common Override Points

| Method | When to Override |
|--------|-----------------|
| `action_confirm` | Add validation before confirm, trigger custom actions after |
| `_prepare_invoice_line` | Pass custom data from SO line to invoice line |
| `_compute_qty_delivered` | Custom delivery quantity computation |
| `_get_invoiced` | Custom invoice matching logic |
| `_compute_invoice_status` | Custom invoicing status rules |
| `_action_confirm` | Internal post-confirmation hooks |

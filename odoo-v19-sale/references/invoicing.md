# Odoo 19 Sale-to-Invoice Flow Reference

## Overview

```
sale.order (confirmed)
  │
  │  _create_invoices(grouped, final, date)
  ▼
sale.order.line
  │
  │  _prepare_invoice_line(**optional_values)
  ▼
account.move (draft invoice)
  │
  │  account.move.line created from SO line values
  ▼
Invoice posted → Payment → Reconciliation
```

## _create_invoices()

**Location**: `sale.order` model
**Signature**:
```python
def _create_invoices(self, grouped=False, final=False, date=None):
```

**Parameters**:
- `grouped` (bool): If True, one invoice per SO. If False, invoices grouped by keys from `_get_invoice_grouping_keys()` (default: partner_id, currency_id, company_id).
- `final` (bool): If True, generates refunds for lines where invoiced qty > delivered qty (used for final invoicing).
- `date` (date): Unused parameter.

**Returns**: `account.move` recordset of created invoices.

**Raises**: `UserError` if no invoiceable lines found.

**Flow**:
1. Collects all SO lines with `qty_to_invoice != 0`
2. Groups lines by invoice grouping keys
3. For each group, creates an `account.move` (draft invoice)
4. Each SO line generates invoice line(s) via `_prepare_invoice_lines_vals_list()`
5. Links invoice lines back to SO lines via `sale_line_ids`
6. Resequences invoice lines to match SO line order
7. Returns created invoices

## _prepare_invoice_line()

**Location**: `sale.order.line` model
**Signature**:
```python
def _prepare_invoice_line(self, **optional_values):
```

**Returns** a dict with values for `account.move.line`:

```python
{
    'display_type': self.display_type or 'product',
    'sequence': self.sequence,
    'name': self.name,
    'product_id': self.product_id.id,
    'product_uom_id': self.product_uom_id.id,
    'quantity': qty_to_invoice,
    'discount': self.discount,
    'price_unit': self.price_unit,
    'tax_ids': [Command.set(self.tax_ids.ids)],
    'sale_line_ids': [Command.link(self.id)],
    # + optional_values merged in
}
```

**Key detail**: `quantity` is set to `self.qty_to_invoice` — the amount not yet invoiced.

### Overriding _prepare_invoice_line

This is the main extension point for passing custom data from SO line to invoice line:

```python
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_ref = fields.Char(string="Custom Reference")

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        # Add custom field to invoice line values
        res['custom_ref'] = self.custom_ref
        return res
```

**Important**: The target field (`custom_ref`) must also exist on `account.move.line`. You need to add it there too:

```python
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    custom_ref = fields.Char(string="Custom Reference")
```

## _get_invoice_grouping_keys()

**Location**: `sale.order` model
**Returns**: List of field names used to group SO lines into invoices.

**Default keys**: `['company_id', 'partner_id', 'currency_id']`

Override to change grouping behavior:

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_invoice_grouping_keys(self):
        keys = super()._get_invoice_grouping_keys()
        keys.append('partner_shipping_id')  # separate invoice per delivery address
        return keys
```

## Invoice Policies

Set on `product.template`:

| Policy | Field | Behavior |
|--------|-------|----------|
| **Ordered Quantities** | `invoice_policy = 'order'` | Invoice full ordered qty immediately |
| **Delivered Quantities** | `invoice_policy = 'delivery'` | Invoice only delivered qty |

This affects `qty_to_invoice` computation on SO lines:
- **order**: `qty_to_invoice = product_uom_qty - qty_invoiced`
- **delivery**: `qty_to_invoice = qty_delivered - qty_invoiced`

## Down Payments

Down payments are special SO lines with `is_downpayment = True`:
- Created via the "Create Invoice" wizard (`sale.advance.payment.inv`)
- Wizard options: Regular invoice, Down payment (percentage), Down payment (fixed amount)
- Down payment lines are deducted from the final invoice

## Invoice Wizard

**Model**: `sale.advance.payment.inv` (TransientModel)
**Action**: `sale.action_view_sale_advance_payment_inv`
**Context**: `{'active_ids': [sale_order_ids]}`

**Options**:
- `advance_payment_method = 'delivered'` → Invoice delivered qty
- `advance_payment_method = 'percentage'` → Down payment by percentage
- `advance_payment_method = 'fixed'` → Down payment by fixed amount

## Linking: SO Line ↔ Invoice Line

The relationship is Many2many via `sale_order_line_invoice_rel`:
- `sale.order.line.invoice_lines` → `account.move.line` records
- `account.move.line.sale_line_ids` → `sale.order.line` records

This allows:
- One SO line to appear on multiple invoices (partial invoicing)
- One invoice line to link to multiple SO lines (grouped invoicing)

## Common Extension Scenarios

### Custom invoice values from SO

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['custom_field'] = self.custom_field
        return res
```

### Prevent invoicing under conditions

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        for order in self:
            if order.custom_check_fails():
                raise UserError(_("Cannot invoice: custom check failed."))
        return super()._create_invoices(grouped=grouped, final=final, date=date)
```

### Custom qty_to_invoice logic

```python
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty', 'state')
    def _compute_qty_to_invoice(self):
        super()._compute_qty_to_invoice()
        for line in self:
            if line.product_id.custom_invoice_rule:
                line.qty_to_invoice = line.custom_computation()
```

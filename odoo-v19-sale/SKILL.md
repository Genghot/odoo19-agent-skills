---
name: odoo-v19-sale
description: >
  Odoo 19 Sale module. sale.order, sale.order.line, quotation workflow
  (draft → sent → sale → cancel), order confirmation, invoicing from sales,
  _create_invoices, _prepare_invoice_line, amount computation, delivery
  integration, pricelist, discount, sale management. Use when working with
  sales, quotations, sale orders, or any module depending on 'sale'.
metadata:
  author: kenghot-king
  version: "1.0"
  odoo-version: "19.0"
  edition: community
---

# Odoo 19 Sale Module

## Business Context

The Sale module manages the sales pipeline from quotation to confirmed order, triggering invoicing and delivery. `sale.order` inherits from `portal.mixin`, `product.catalog.mixin`, `mail.thread`, `mail.activity.mixin`, `utm.mixin`, and `account.document.import.mixin`.

Module dependency: `depends: ['sales_team', 'account_payment', 'utm']`

## Workflow

```
                    action_quotation_sent()
  ┌─────────┐  ──────────────────────────►  ┌──────────┐
  │  draft  │                                │   sent   │
  │Quotation│  ◄──────────────────────────  │Quot. Sent│
  └────┬────┘       action_draft()           └────┬─────┘
       │                                          │
       │         action_confirm()                 │
       ├──────────────────────────────────────────┤
       │                                          │
       ▼                                          ▼
  ┌──────────┐                              ┌──────────┐
  │   sale   │  ── action_lock() ──►        │  cancel  │
  │Sales Ord.│  ◄─ action_unlock() ─        │Cancelled │
  │(locked)  │                              └──────────┘
  └──────────┘        ▲
                      │ action_cancel()
                      │ (from draft/sent/sale)
```

**States**: `draft` (Quotation), `sent` (Quotation Sent), `sale` (Sales Order), `cancel` (Cancelled).

**Key transitions**:
- `action_confirm()` → sets state to `'sale'`, sets `date_order`, triggers downstream (stock picking via sale_stock, etc.)
- `action_cancel()` → cancels order and related draft invoices
- `action_draft()` → returns cancelled/sent orders to draft
- `action_lock()` / `action_unlock()` → prevents/allows modifications on confirmed orders

## Key Models

### sale.order

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Order reference (auto-sequence) |
| `partner_id` | Many2one(res.partner) | Customer |
| `date_order` | Datetime | Order/confirmation date |
| `state` | Selection | draft/sent/sale/cancel |
| `locked` | Boolean | Prevent modifications |
| `order_line` | One2many(sale.order.line) | Order lines |
| `amount_untaxed` | Monetary | Untaxed total (computed, stored) |
| `amount_tax` | Monetary | Tax amount (computed, stored) |
| `amount_total` | Monetary | Grand total (computed, stored) |
| `invoice_ids` | Many2many(account.move) | Related invoices |
| `invoice_status` | Selection | no/to invoice/invoiced/upselling |
| `pricelist_id` | Many2one(product.pricelist) | Pricelist |
| `currency_id` | Many2one(res.currency) | Currency |
| `payment_term_id` | Many2one(account.payment.term) | Payment terms |
| `fiscal_position_id` | Many2one(account.fiscal.position) | Fiscal position |
| `user_id` | Many2one(res.users) | Salesperson |
| `team_id` | Many2one(crm.team) | Sales team |
| `partner_invoice_id` | Many2one(res.partner) | Invoice address |
| `partner_shipping_id` | Many2one(res.partner) | Delivery address |
| `validity_date` | Date | Expiration date |
| `note` | Html | Terms and conditions |
| `tag_ids` | Many2many(crm.tag) | Tags |
| `client_order_ref` | Char | Customer reference |
| `origin` | Char | Source document |
| `company_id` | Many2one(res.company) | Company |

See `references/models.md` for complete field list.

### sale.order.line

| Field | Type | Description |
|-------|------|-------------|
| `order_id` | Many2one(sale.order) | Parent order |
| `product_id` | Many2one(product.product) | Product |
| `name` | Text | Description |
| `product_uom_qty` | Float | Ordered quantity |
| `product_uom_id` | Many2one(uom.uom) | Unit of measure |
| `price_unit` | Float | Unit price |
| `discount` | Float | Discount (%) |
| `tax_ids` | Many2many(account.tax) | Taxes |
| `price_subtotal` | Monetary | Subtotal excl. tax (computed, stored) |
| `price_tax` | Float | Tax amount (computed, stored) |
| `price_total` | Monetary | Total incl. tax (computed, stored) |
| `qty_delivered` | Float | Delivered quantity |
| `qty_invoiced` | Float | Invoiced quantity (computed, stored) |
| `qty_to_invoice` | Float | Qty to invoice (computed, stored) |
| `invoice_status` | Selection | Invoicing status per line |
| `invoice_lines` | Many2many(account.move.line) | Related invoice lines |
| `display_type` | Selection | line_section/line_subsection/line_note |
| `is_downpayment` | Boolean | Down payment line |
| `customer_lead` | Float | Lead time (days) |
| `sequence` | Integer | Display order |

## Amount Computation

```
sale.order.line._compute_amount()
  └── Depends on: product_uom_qty, discount, price_unit, tax_ids
  └── Computes: price_subtotal, price_tax, price_total
  └── Uses AccountTax for tax computation

sale.order._compute_amounts()
  └── Depends on: order_line.price_subtotal, currency_id, company_id
  └── Computes: amount_untaxed, amount_tax, amount_total
  └── Sums line subtotals + tax totals
```

All amount fields are `store=True` computed fields — they update automatically when lines change.

## Extension Patterns

### Add a field to sale.order

```python
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char(string="Custom Field")
```

### Hook into order confirmation

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            if not order.custom_field:
                raise UserError(_("Custom field required before confirmation."))
        res = super().action_confirm()
        # Post-confirmation logic
        return res
```

### Pass custom data from SO line to invoice line

```python
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_field = fields.Char(string="Custom")

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res['custom_field'] = self.custom_field
        return res
```

### Extend sale order form view (XPath)

```xml
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit.my_module</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='payment_term_id']" position="after">
            <field name="custom_field"/>
        </xpath>
    </field>
</record>
```

## Common Pitfalls

1. **Forgetting `super()` in `action_confirm`** — skipping it breaks stock picking creation (via `sale_stock`), invoice triggering, and any other module hooking into confirmation.
2. **Modifying `amount_total` directly** — it's a stored computed field. Modify line-level values (qty, price, discount, tax) instead; totals recompute automatically.
3. **Using `@api.onchange` for SO line amounts** — SO line amounts (`price_subtotal`, `price_total`) are computed fields, not onchange. Adding onchange for these won't trigger on programmatic writes.
4. **Not handling `display_type`** — SO lines can be sections (`line_section`), subsections (`line_subsection`), or notes (`line_note`). These have no product/amount. Filter them: `line.display_type == False`.
5. **Multi-company issues** — `sale.order` has `_check_company_auto = True`. Custom relational fields should include `check_company=True` if they reference company-specific records.
6. **Ignoring `locked` state** — after `action_lock()`, the order shouldn't be modified. Check `locked` in custom write logic.

## Sub-module Map

| Module | Description | Auto-install |
|--------|-------------|--------------|
| `sale_stock` | Delivery integration — creates `stock.picking` from confirmed SO | Yes (sale + stock_account) |
| `sale_management` | Quotation templates, full sales app UI | No (application) |
| `sale_project` | Task/project generation from SO lines | Yes (sale_management + project_account) |
| `sale_mrp` | Manufacturing orders from sales | Yes (mrp + sale_stock) |
| `sale_purchase` | Service outsourcing — auto-creates PO from SO | Yes (sale + purchase) |

## References

- `references/models.md` — Complete field lists for sale.order and sale.order.line
- `references/order-workflow.md` — Detailed state transitions and method signatures
- `references/invoicing.md` — Sale-to-invoice flow, _create_invoices, _prepare_invoice_line
- See also: `odoo-v19-core` (ORM, inheritance), `odoo-v19-views` (view extension patterns)

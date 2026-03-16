# Odoo 19 Sale Models Reference

## sale.order — Complete Field List

| Field | Type | Key Parameters |
|-------|------|----------------|
| `name` | Char | required, readonly=False, index='trigram' |
| `company_id` | Many2one(res.company) | required, index |
| `partner_id` | Many2one(res.partner) | required, tracking=1, change_default |
| `state` | Selection | draft/sent/sale/cancel, readonly, copy=False, tracking=3 |
| `locked` | Boolean | default=False, copy=False, tracking |
| `client_order_ref` | Char | copy=False |
| `create_date` | Datetime | readonly |
| `commitment_date` | Datetime | copy=False |
| `date_order` | Datetime | required, copy=False, default=now |
| `origin` | Char | Source Document |
| `reference` | Char | Payment Ref, copy=False |
| `require_signature` | Boolean | compute, store, readonly=False, precompute |
| `require_payment` | Boolean | compute, store, readonly=False, precompute |
| `prepayment_percent` | Float | compute, store, readonly=False, precompute |
| `signature` | Image | copy=False, max_width=1024, max_height=1024 |
| `signed_by` | Char | copy=False |
| `signed_on` | Datetime | copy=False |
| `validity_date` | Date | compute, store, readonly=False, copy=False, precompute |
| `journal_id` | Many2one(account.journal) | compute, store, readonly=False, precompute |
| `note` | Html | compute, store, readonly=False, precompute |
| `partner_invoice_id` | Many2one(res.partner) | compute, store, required, precompute, check_company |
| `partner_shipping_id` | Many2one(res.partner) | compute, store, required, precompute, check_company |
| `fiscal_position_id` | Many2one(account.fiscal.position) | compute, store, readonly=False, precompute, check_company |
| `payment_term_id` | Many2one(account.payment.term) | compute, store, readonly=False, precompute, check_company |
| `preferred_payment_method_line_id` | Many2one(account.payment.method.line) | compute, store, precompute, readonly=False, check_company |
| `pricelist_id` | Many2one(product.pricelist) | compute, store, readonly=False, precompute, check_company, tracking=1 |
| `currency_id` | Many2one(res.currency) | compute, store, precompute |
| `currency_rate` | Float | compute, store, precompute |
| `user_id` | Many2one(res.users) | compute, store, readonly=False, precompute, index, tracking=2 |
| `team_id` | Many2one(crm.team) | compute, store, readonly=False, precompute, check_company, tracking |
| `order_line` | One2many(sale.order.line) | copy=True |
| `amount_untaxed` | Monetary | compute='_compute_amounts', store, tracking=5 |
| `amount_tax` | Monetary | compute='_compute_amounts', store |
| `amount_total` | Monetary | compute='_compute_amounts', store, tracking=4 |
| `amount_to_invoice` | Monetary | compute='_compute_amount_to_invoice' |
| `amount_invoiced` | Monetary | compute='_compute_amount_invoiced' |
| `invoice_count` | Integer | compute='_get_invoiced' |
| `invoice_ids` | Many2many(account.move) | compute='_get_invoiced', search='_search_invoice_ids', copy=False |
| `invoice_status` | Selection | upselling/invoiced/to invoice/no, compute, store |
| `transaction_ids` | Many2many(payment.transaction) | copy=False, readonly |
| `amount_paid` | Float | compute, compute_sudo |
| `tag_ids` | Many2many(crm.tag) | groups="sales_team.group_sale_salesman" |
| `amount_undiscounted` | Float | compute |
| `country_code` | Char | related='company_id.account_fiscal_country_id.code' |
| `expected_date` | Datetime | compute, store=False |
| `is_expired` | Boolean | compute |
| `type_name` | Char | compute (returns "Quotation" or "Sales Order") |
| `tax_totals` | Binary | compute, exportable=False |
| `show_update_fpos` | Boolean | store=False |
| `show_update_pricelist` | Boolean | store=False |

## sale.order.line — Complete Field List

| Field | Type | Key Parameters |
|-------|------|----------------|
| `order_id` | Many2one(sale.order) | required, ondelete='cascade', index |
| `sequence` | Integer | default=10 |
| `company_id` | Many2one(res.company) | related='order_id.company_id', store, precompute |
| `currency_id` | Many2one(res.currency) | related='order_id.currency_id', store, precompute |
| `order_partner_id` | Many2one(res.partner) | related='order_id.partner_id', store, precompute |
| `salesman_id` | Many2one(res.users) | related='order_id.user_id', store, precompute |
| `state` | Selection | related='order_id.state', store, precompute |
| `display_type` | Selection | line_section/line_subsection/line_note, default=False |
| `is_downpayment` | Boolean | |
| `is_expense` | Boolean | |
| `product_id` | Many2one(product.product) | change_default, ondelete='restrict', check_company |
| `product_template_id` | Many2one(product.template) | compute, readonly=False |
| `name` | Text | compute, store, readonly=False, required, precompute |
| `product_uom_qty` | Float | compute, store, readonly=False, required, default=1.0, precompute |
| `product_uom_id` | Many2one(uom.uom) | compute, store, readonly=False, precompute |
| `tax_ids` | Many2many(account.tax) | compute, store, readonly=False, precompute, check_company |
| `pricelist_item_id` | Many2one(product.pricelist.item) | compute |
| `price_unit` | Float | compute, store, readonly=False, required, precompute |
| `discount` | Float | compute, store, readonly=False, precompute |
| `price_subtotal` | Monetary | compute='_compute_amount', store, precompute |
| `price_tax` | Float | compute='_compute_amount', store, precompute |
| `price_total` | Monetary | compute='_compute_amount', store, precompute |
| `price_reduce_taxexcl` | Monetary | compute, store, precompute |
| `price_reduce_taxinc` | Monetary | compute, store, precompute |
| `customer_lead` | Float | compute, store, readonly=False, required, precompute |
| `qty_delivered_method` | Selection | manual/analytic, compute, store, precompute |
| `qty_delivered` | Float | compute, store, readonly=False, copy=False |
| `qty_invoiced` | Float | compute, store |
| `qty_to_invoice` | Float | compute, store |
| `invoice_lines` | Many2many(account.move.line) | copy=False |
| `invoice_status` | Selection | compute, store |
| `untaxed_amount_invoiced` | Monetary | compute, store |
| `untaxed_amount_to_invoice` | Monetary | compute, store |
| `analytic_line_ids` | One2many(account.analytic.line) | |
| `linked_line_id` | Many2one(sale.order.line) | ondelete='cascade', copy=False |
| `combo_item_id` | Many2one(product.combo.item) | |
| `product_type` | Selection | related='product_id.type' |
| `product_updatable` | Boolean | compute |
| `product_uom_readonly` | Boolean | compute |
| `parent_id` | Many2one(sale.order.line) | compute (parent section line) |
| `collapse_prices` | Boolean | default=False |
| `collapse_composition` | Boolean | default=False |

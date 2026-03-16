## ADDED Requirements

### Requirement: Sale SKILL.md with smart description
The skill SHALL have a SKILL.md file with YAML frontmatter containing `name: odoo-v19-sale`, a description that includes keywords: sale.order, sale.order.line, quotation, sales order, order confirmation, invoicing from sales, delivery integration, sale module, product pricing, pricelist, discount, sale workflow. The description SHALL be under 1024 characters.

#### Scenario: Agent activates on quotation query
- **WHEN** a user asks "add a discount field to the quotation"
- **THEN** the agent matches "quotation", "sale.order", "discount" and loads the odoo-v19-sale skill

#### Scenario: Agent activates on sale module dependency
- **WHEN** a user asks "my module depends on sale, how do I extend sale.order?"
- **THEN** the agent matches "sale.order", "sale module" and loads the skill

### Requirement: Business Context section
The SKILL.md body SHALL explain the sale module's business purpose: managing the sales pipeline from quotation to confirmed order, triggering invoicing and delivery. It SHALL note that `sale.order` inherits from `portal.mixin`, `mail.thread`, `mail.activity.mixin`, `utm.mixin`, and `account.document.import.mixin`.

#### Scenario: Agent understands sale module purpose
- **WHEN** the skill is activated
- **THEN** the agent knows the sale module handles quotation → order → invoice/delivery flow

### Requirement: Workflow documentation with state diagram
The SKILL.md SHALL include an ASCII state diagram showing the sale order lifecycle: `draft` (Quotation) → `sent` (Quotation Sent) → `sale` (Sales Order) → `done` (Locked) / `cancel` (Cancelled). It SHALL document the key transition methods: `action_quotation_sent`, `action_confirm`, `action_cancel`, `action_draft`, `action_lock`, `action_unlock`.

#### Scenario: Developer hooks into order confirmation
- **WHEN** user asks "run custom logic when a quotation is confirmed"
- **THEN** the skill shows that `action_confirm` is the method to override, transitioning state from draft/sent to sale

### Requirement: Key Models documentation
The SKILL.md SHALL document `sale.order` and `sale.order.line` with their key fields:

For `sale.order`: `name`, `partner_id`, `date_order`, `state`, `amount_untaxed`, `amount_tax`, `amount_total`, `order_line`, `invoice_ids`, `pricelist_id`, `currency_id`, `company_id`, `user_id`, `team_id`, `invoice_status`.

For `sale.order.line`: `order_id`, `product_id`, `product_uom_qty`, `product_uom`, `price_unit`, `discount`, `tax_id`, `price_subtotal`, `price_total`, `qty_delivered`, `qty_invoiced`, `qty_to_invoice`.

#### Scenario: Developer adds a field to sale order
- **WHEN** user asks "add a custom field to sale.order"
- **THEN** the skill provides the model name, existing key fields, and the `_inherit = 'sale.order'` pattern

### Requirement: Amount computation documentation
The SKILL.md SHALL explain how `amount_untaxed`, `amount_tax`, and `amount_total` are computed from order lines, including the `_compute_amounts` method and the line-level `_compute_amount` method. It SHALL note these are `store=True` computed fields triggered by line changes.

#### Scenario: Developer understands price computation
- **WHEN** user asks "how is the total calculated on a sale order?"
- **THEN** the skill explains the computation chain: line amounts → order amounts, all stored computed fields

### Requirement: Extension Patterns section
The SKILL.md SHALL document common extension patterns:
- Adding fields to `sale.order` or `sale.order.line`
- Hooking into `action_confirm` (override with `super()`)
- Customizing `_prepare_invoice_line` (for invoice generation)
- Extending sale order views via XPath (reference to odoo-v19-views)
- Adding sale order line compute fields

#### Scenario: Developer customizes invoice generation
- **WHEN** user asks "pass a custom field from SO line to invoice line"
- **THEN** the skill shows the `_prepare_invoice_line` override pattern

### Requirement: Common Pitfalls section
The SKILL.md SHALL include at least 4 pitfalls: forgetting to call `super()` in `action_confirm` (breaks stock picking creation), modifying `amount_total` directly instead of through line computation, not handling multi-company in custom fields, and using `@api.onchange` for fields that should be computed (sale.order.line amounts are computed, not onchange).

#### Scenario: Agent avoids breaking order confirmation
- **WHEN** the agent overrides `action_confirm`
- **THEN** it always calls `super()` because the pitfalls section warns that skipping it breaks delivery and invoice flows

### Requirement: Sub-module Map
The SKILL.md SHALL list key modules that extend sale: `sale_stock` (delivery integration), `sale_management` (quotation templates), `sale_project` (project/task generation), `sale_mrp` (manufacturing from sales), `sale_purchase` (dropshipping/buy-to-order), with a one-line description of what each adds.

#### Scenario: Developer understands module dependencies
- **WHEN** user asks "how does sale connect to inventory?"
- **THEN** the skill points to `sale_stock` and its role in creating `stock.picking` from confirmed sale orders

### Requirement: Reference files for deep content
The skill SHALL include reference files: `references/models.md` (complete field lists for sale.order and sale.order.line with types and descriptions), `references/order-workflow.md` (detailed workflow with method signatures and hook points), `references/invoicing.md` (sale-to-invoice flow, `_create_invoices` method, `_prepare_invoice_line` details).

#### Scenario: Agent needs full field list
- **WHEN** the agent needs to know all fields on sale.order.line
- **THEN** it reads `references/models.md` which lists every field with its type, string, and key parameters

### Requirement: Token budget compliance
The SKILL.md body SHALL be under 5000 tokens (~400 lines). Each reference file SHALL be under 3000 tokens (~250 lines).

#### Scenario: Skill fits context budget
- **WHEN** the agent activates the skill
- **THEN** the SKILL.md loads within the 5K token budget

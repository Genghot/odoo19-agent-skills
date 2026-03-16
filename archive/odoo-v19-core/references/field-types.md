# Odoo 19 Field Types Reference

## Common Parameters (All Fields)

| Parameter | Type | Description |
|-----------|------|-------------|
| `string` | str | UI label |
| `help` | str | Tooltip text |
| `readonly` | bool | Read-only in UI and code |
| `required` | bool | Must have a value |
| `index` | `'btree'`\|`'btree_not_null'`\|`'trigram'`\|`False` | DB index type |
| `default` | value or callable | Default value (callable receives `self`) |
| `groups` | str | Comma-separated group XML IDs for field access |
| `company_dependent` | bool | Different value per company |
| `copy` | bool | Include when duplicating record |
| `store` | bool | Persist to DB (default True, False for non-stored compute) |
| `compute` | str | Method name for computed value |
| `precompute` | bool | Compute before first DB insert |
| `compute_sudo` | bool | Compute with superuser privileges |
| `inverse` | str | Method name for writing back computed value |
| `search` | str | Method name for custom search logic |
| `related` | str | Shortcut for related field (e.g., `'order_id.partner_id'`) |
| `aggregator` | str | `'sum'`\|`'avg'`\|`'min'`\|`'max'`\|`'count'`\|`'count_distinct'`\|`'bool_and'`\|`'bool_or'` |
| `recursive` | bool | Compute depends on self (tree structures) |
| `translate` | bool or callable | Enable translation |
| `group_expand` | callable or True | Expand groups in group_by views |

## Scalar Fields

### Char
```python
fields.Char(string="Name", size=None, trim=True, translate=False)
```
- `size`: Max length (None = unlimited)
- `trim`: Strip whitespace (default True)

### Text
```python
fields.Text(string="Description", translate=False)
```
Multiline text. Same as Char but no `size` and renders as textarea.

### Html
```python
fields.Html(string="Body", sanitize=True, sanitize_tags=True, sanitize_attributes=True,
            sanitize_style=False, strip_style=False, strip_classes=False)
```
HTML content with built-in sanitization.

### Integer
```python
fields.Integer(string="Count")
```
Python int. Falsy value = 0.

### Float
```python
fields.Float(string="Amount", digits=(16, 2))
# or use named precision:
fields.Float(string="Weight", digits='Stock Weight')
```
- `digits`: Tuple `(precision, scale)` or string referencing `decimal.precision` record

### Monetary
```python
fields.Monetary(string="Total", currency_field='currency_id')
```
- `currency_field`: Name of Many2one field pointing to `res.currency` (default `'currency_id'`)

### Boolean
```python
fields.Boolean(string="Active", default=True)
```

### Date
```python
fields.Date(string="Start Date")
```
Static methods: `Date.today()`, `Date.context_today(record)`, `Date.to_date(value)`, `Date.to_string(value)`

### Datetime
```python
fields.Datetime(string="Created On")
```
Static methods: `Datetime.now()`, `Datetime.context_timestamp(record, timestamp)`, `Datetime.to_datetime(value)`

### Selection
```python
fields.Selection(
    selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')],
    string="Status", default='draft'
)
# Extend in inherited model:
state = fields.Selection(selection_add=[('custom', 'Custom')], ondelete={'custom': 'set default'})
```
- `selection`: List of `(value, label)` tuples, or method name, or callable
- `selection_add`: Extend parent selection (insertion order matters)
- `ondelete`: Dict mapping value → action when option removed (`'set null'`\|`'set default'`\|`'cascade'`)

### Binary
```python
fields.Binary(string="File", attachment=True)
```
- `attachment`: Store as `ir.attachment` (default True) vs bytea column

### Image
```python
fields.Image(string="Photo", max_width=1024, max_height=1024, verify_resolution=True)
```
Extends Binary. Auto-resizes maintaining aspect ratio.

### Json
```python
fields.Json(string="Metadata")
```
Stores arbitrary JSON. Maps to JSONB in PostgreSQL.

## Relational Fields

### Many2one
```python
fields.Many2one('res.partner', string="Customer", ondelete='set null',
                domain=[('is_company', '=', True)], check_company=True)
```
- `comodel_name`: Target model (first positional arg)
- `ondelete`: `'set null'` (default) | `'restrict'` | `'cascade'`
- `domain`: Static or dynamic domain
- `check_company`: Validate company consistency
- `delegate`: True for `_inherits` fields (auto-set)

### One2many
```python
fields.One2many('sale.order.line', 'order_id', string="Order Lines")
```
- `comodel_name`: Target model
- `inverse_name`: Many2one field on target pointing back
- `copy`: Default False

### Many2many
```python
fields.Many2many('account.tax', string="Taxes",
                 relation='sale_order_line_tax_rel',  # junction table name
                 column1='line_id', column2='tax_id')
```
- `relation`: Custom junction table name (auto-generated if omitted)
- `column1`: FK column for this model
- `column2`: FK column for comodel

### Reference
```python
fields.Reference(selection=[('res.partner', 'Partner'), ('res.users', 'User')],
                 string="Related Document")
```
Stored as `"model_name,record_id"` string. No FK constraint.

### Many2oneReference
```python
res_id = fields.Many2oneReference(string="Record ID", model_field='res_model')
res_model = fields.Char(string="Model Name")
```
- `model_field`: Char field storing the model name. Integer field storing the record ID.

## Special Fields

### Properties
```python
fields.Properties(string="Custom Properties", definition='parent_id.properties_definition')
```
Dynamic fields defined by a parent record. Stored as JSONB.

### fields.Command (for One2many/Many2many writes)

```python
from odoo.fields import Command
# In create/write vals:
'line_ids': [
    Command.create({'name': 'New line'}),        # (0, 0, vals)
    Command.update(id, {'name': 'Updated'}),     # (1, id, vals)
    Command.delete(id),                           # (2, id, 0)
    Command.unlink(id),                           # (3, id, 0)
    Command.link(id),                             # (4, id, 0)
    Command.clear(),                              # (5, 0, 0)
    Command.set([id1, id2]),                      # (6, 0, [ids])
]
```

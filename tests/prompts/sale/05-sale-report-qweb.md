# Test: Sale Report / QWeb

## Prompt

```
Create a new Odoo 19 module called "sale_custom_report" in addons/.
It should:
1. Add a custom section to the sale order PDF report that shows:
   - A "Terms and Conditions" header
   - The sale order's note field content
   - A table showing payment term details
2. This should appear after the existing order lines table in the report
```

## Verify

- [ ] Inherits `sale.report_saleorder_document` via `inherit_id`
- [ ] Uses XPath to target correct element in the report template
- [ ] QWeb template uses `t-if`, `t-foreach`, `t-esc` correctly
- [ ] Report XML loaded in `data` section of manifest
- [ ] Module installs in Docker without errors

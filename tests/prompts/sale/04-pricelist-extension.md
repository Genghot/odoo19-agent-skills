# Test: Pricelist Extension

## Prompt

```
Create a new Odoo 19 module called "sale_pricelist_note" in addons/.
It should:
1. Add a "internal_note" Text field to product.pricelist
2. Add a "discount_reason" Char field to product.pricelist.item
3. Show both fields in their respective form views (inherit existing views)
4. Add discount_reason as a column in the pricelist item list within
   the pricelist form
```

## Verify

- [ ] `_inherit = 'product.pricelist'` and `_inherit = 'product.pricelist.item'`
- [ ] Correct parent views inherited (from `product` module)
- [ ] XPath targets valid elements in pricelist views
- [ ] Fields have proper string labels
- [ ] Module installs in Docker without errors

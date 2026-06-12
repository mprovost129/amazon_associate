# Phase 4 Summary — Scaling & Operations

This package builds on Phase 3 and adds operational tooling for managing a larger affiliate/content site.

## Added

- Product CSV export for staff users.
- Product CSV import for staff users.
- Admin CSV template download.
- Product admin bulk actions:
  - mark current/reviewed
  - mark needs review
  - deactivate/archive
  - export selected products
- Product review workflow fields:
  - `review_status`
  - `review_notes`
  - `next_review_at`
  - `last_checked_at`
  - `amazon_asin`
- Manual related products field for stronger internal linking.
- Product detail pages now prefer hand-picked related products before fallback category products.
- Staff import/export routes:
  - `/products/import/`
  - `/products/export/`

## After deploying

Run:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Suggested workflow

1. Download the CSV template from Products admin.
2. Fill in products offline.
3. Import using `/products/import/`.
4. Use admin filters to review products by status and next review date.
5. Add hand-picked related products to your strongest product/detail pages.

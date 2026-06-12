# Phase 2 Summary

This package builds on the Phase 1 launch-readiness work and adds the content/funnel layer needed for a traffic-driven affiliate site.

## Added

### Guides / Articles
- New `guides` app.
- `Guide` model with title, slug, summary, category, tags, body, related products, featured image URL, publish flags, SEO title/description, and timestamps.
- Guide list and detail pages.
- Guide admin with filters, featured/published controls, tags, and related products.
- Guide sitemap support.

### Collections / Kits
- New `Collection` model in `products`.
- Collection list and detail pages.
- Admin support for published/featured collections and product assignment.
- Collection sitemap support.

### Tags / Use Cases
- New `Tag` model in `products`.
- Products can now be tagged by use case such as beginner, desk setup, 3D printing, measuring, coding, etc.
- Tags display on product cards and can be used as search filters.

### Search and Filtering
- New `/products/` search page.
- Search by keyword across product name, description, best-for text, recommendation copy, category, and tags.
- Filter by category and tag/use case.
- Pagination added to search results.

### Homepage Funnel
- Reworked homepage into a stronger traffic landing page.
- Adds workflow entry points for:
  - Home design tools
  - Construction/jobsite picks
  - Coding/web design setup
  - 3D printing gear
- Adds featured guides section.
- Adds featured collections/kits section.
- Adds use-case tag browsing.
- Keeps featured products and category product sections.

### Navigation and Footer
- Navbar now links to Guides, Collections, All Picks, and category pages.
- Navbar includes sitewide product search.
- Footer now links to Guides, Collections, and All Picks.

## New URLs

- `/guides/`
- `/guides/<slug>/`
- `/collections/`
- `/collections/<slug>/`
- `/products/`
- `/products/?q=3d+printing`
- `/products/?category=<category-slug>`
- `/products/?tag=<tag-slug>`

## Migration Files

- `products/migrations/0005_tags_collections.py`
- `guides/migrations/0001_initial.py`

## After Installing

Run:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Then create a few tags, guides, and collections in Django admin.

Suggested first tags:

- beginner
- budget
- desk setup
- 3d printing
- home design
- construction
- coding
- web design
- measuring
- tools

Suggested first collections:

- Beginner 3D Printing Kit
- Web Design Desk Setup
- Home Design Tools
- Construction Measuring Kit

Suggested first guides:

- The 10 Tools I’d Buy First for 3D Printing
- My Basic Web Design Desk Setup
- Useful Tools for Reviewing House Plans
- Affordable Measuring Tools for Home Design and Construction

## Validation

Python syntax was checked with `python -m compileall`.

`python manage.py check` could not be run in this environment because Django is not installed in the container.

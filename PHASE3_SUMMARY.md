# Phase 3 Summary — Analytics & Performance Tracking

Phase 3 builds on Phase 2 and adds Google Analytics plus first-party attribution for outbound Amazon clicks.

## Added

- Google Analytics support through `GOOGLE_ANALYTICS_ID` or `GA_MEASUREMENT_ID` environment variable.
- Reusable `templates/partials/google_analytics.html` partial included in `base.html`.
- Frontend `affiliate_click` GA event tracking for Amazon CTA clicks.
- Session-based campaign capture middleware for UTM parameters:
  - `utm_source`
  - `utm_medium`
  - `utm_campaign`
  - `utm_term`
  - `utm_content`
- Product click attribution fields:
  - source
  - medium
  - campaign
  - term
  - content
  - landing_page
  - page_path
- Staff-only performance dashboard at `/performance/`.
- Admin improvements for viewing/filtering click source, medium, campaign, and page path.
- Privacy policy note for Google Analytics.
- Render blueprint placeholder for `GOOGLE_ANALYTICS_ID`.

## Setup

Add your Google Analytics Measurement ID in production:

```bash
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
```

or:

```bash
GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

Then run:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Recommended UTM Examples

Use these when posting links on socials:

```text
?utm_source=facebook&utm_medium=social&utm_campaign=3d_printing_tools
?utm_source=instagram&utm_medium=social&utm_campaign=web_design_setup
?utm_source=threads&utm_medium=social&utm_campaign=home_design_tools
```

The middleware stores the campaign in the visitor session, so later outbound product clicks can still be attributed.

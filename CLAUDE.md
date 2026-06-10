# Amazon Associate Storefront

A Django-based Amazon Associates affiliate storefront. Products are managed through the Django admin and displayed as a card grid on the home page.

## Stack

- **Python 3.13** / **Django 6.0.6**
- **PostgreSQL 16** (database)
- **Redis 7** (cache — local memory in dev, Redis in prod)
- **Bootstrap 5.3.3** + **Bootstrap Icons 1.11.3** (frontend)
- **Whitenoise** (static files in production)
- **Gunicorn** (WSGI server)
- **Docker / docker-compose** for local dev

## Project Structure

```
config/
  Settings/
    base.py       # shared settings
    dev.py        # DEBUG=True, debug_toolbar, no password validation
    prod.py       # Whitenoise, Redis cache, HTTPS/HSTS, strict env checks
  urls.py         # root URL config
core/             # home page app
  views.py        # HomeView (ListView of active products)
  urls.py         # app_name='core', route: '' -> core:home
products/         # product catalog app
  models.py       # Product model
  admin.py        # admin with inline editing
  migrations/
users/            # custom user model (email-based auth, no username)
templates/
  base.html       # Bootstrap navbar (dark) + 3-col footer
  core/
    home.html     # 4-column product card grid
static/
  css/main.css    # CSS variables, card styles, footer styles
```

## Apps

### `products`

The core data model. Add and manage products via `/admin/`.

**Product fields:**
| Field | Type | Notes |
|---|---|---|
| `name` | CharField(200) | displayed as card title |
| `description` | TextField | optional, clamped to 3 lines on card |
| `amazon_url` | URLField | full affiliate link with `tag=` parameter |
| `image_url` | URLField | direct image URL; shows placeholder if blank |
| `is_active` | BooleanField | controls visibility on storefront |
| `order` | PositiveIntegerField | lower = appears first; editable inline in admin |
| `created_at` | DateTimeField | auto-set on creation |

Default ordering: `order` ASC, `created_at` DESC.

### `core`

Single view (`HomeView`) that renders all active products as a 4-column Bootstrap card grid.

### `users`

Custom user model using `email` as the username field. No changes needed here for the storefront.

## Running Locally

### With Docker (recommended)

```bash
docker-compose up
```

Runs Postgres, Redis, and the Django dev server at `http://localhost:8000`.

### Without Docker

```bash
pip install -r requirements.txt
# set DJANGO_SETTINGS_MODULE=config.Settings.dev in your shell or .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Requires a local Postgres instance with credentials matching `.env`.

## Environment Variables

Copy `.env.example` to `.env`. Required variables:

| Variable | Notes |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DB_NAME` | Postgres database name |
| `DB_USER` | Postgres user |
| `DB_PASSWORD` | Postgres password |
| `DB_HOST` | Defaults to `localhost` |
| `DB_PORT` | Defaults to `5432` |

Production also requires: `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `REDIS_URL`.

## Settings Module

Always set `DJANGO_SETTINGS_MODULE` explicitly:

- Dev: `config.Settings.dev`
- Prod: `config.Settings.prod`

## Adding Products

1. Go to `/admin/` → Products → Add Product
2. Paste the Amazon affiliate URL (must include your `tag=` parameter)
3. Paste a direct image URL (from Amazon's CDN or S3)
4. Set `is_active = True` and an `order` value
5. Save — appears on the home page immediately

## Amazon Associates Rules

- Affiliate disclosure is in the footer of every page (required).
- All product links use `target="_blank" rel="noopener sponsored"`.
- Do not place affiliate links in emails or push notifications.
- Account requires 3 qualifying sales within the first 180 days or it closes.

## What's Been Built

- [x] Django project scaffold with custom user model, Postgres, Redis, docker-compose
- [x] `products` app — `Product` model, admin with inline editing
- [x] Home page — 4-column Bootstrap card grid (responsive: 4 → 2 → 1)
- [x] Product cards — square image area, title, description, "View on Amazon" button, placeholder if no image
- [x] Bootstrap navbar — dark, collapsible on mobile, active-link highlighting
- [x] Footer — 3-column (brand, links, affiliate disclosure), sticky to bottom
- [x] Production settings — Whitenoise, Redis cache, HTTPS/HSTS hardening
- [x] `Category` model — name + slug, FK on `Product` (nullable)
- [x] Category filter bar — pill buttons above grid, `/?category=<slug>` query param
- [x] Click tracking — `ProductClick` model records every outbound click (referrer, user-agent, hashed IP); redirect view at `/go/<pk>/`
- [x] Admin — click count column on Product list, read-only ProductClick log, CategoryAdmin with slug auto-fill

## Click Tracking

All product links route through `/go/<pk>/` (`products:redirect`). The redirect view:
1. Logs a `ProductClick` row (referrer, user-agent, SHA-256 hashed IP)
2. Issues a 302 to `product.amazon_url`

View click data at `/admin/products/productclick/`. Click counts appear in the Product list column.

## Deploying to Render

The project includes a `render.yaml` Blueprint. Steps:

1. Push the repo to GitHub
2. In Render dashboard → New → Blueprint → connect the repo
3. Render auto-creates the web service + PostgreSQL database
4. After first deploy, set these env vars manually in the Render dashboard:
   - `ALLOWED_HOSTS` → `your-app-name.onrender.com` (or custom domain)
   - `CSRF_TRUSTED_ORIGINS` → `https://your-app-name.onrender.com`
5. Redeploy — the app will be live

**Notes:**
- `SECRET_KEY` is auto-generated by Render (`generateValue: true`)
- Migrations run automatically via `preDeployCommand` before each deploy
- Redis is optional — omit `REDIS_URL` to use in-memory cache (fine for low traffic)
- Render's free PostgreSQL expires after 90 days; upgrade to Starter ($7/mo) for persistence
- Static files are served by Whitenoise — no S3 needed

## What's Not Built Yet

- Product detail page (longer copy, per-product SEO)
- SEO metadata per product
- `robots.txt` (exclude `/admin/`, `/go/`, `/accounts/`)
- Search
- Featured / spotlight section

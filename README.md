# Photography Business Website

Flask + MongoDB Atlas + Tailwind CSS (compiled build, no CDN dependency).

## First-time setup

```bash
# 1. Python environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt

# 2. Frontend build (Tailwind CSS - REQUIRED before first run)
npm install
npm run build:css

# 3. Environment variables
cp .env.example .env
# then edit .env with your real MONGO_URI and SECRET_KEY

# 4. Seed the database (creates your admin login)
python -m database.seed

# 5. Run
python run.py
```

Visit `http://localhost:5000` for the public site, `http://localhost:5000/admin/login` for the admin panel.

## After changing templates

If you add new Tailwind classes to any `.html` file, recompile CSS:

```bash
npm run build:css
```

Or run `npm run watch:css` in a separate terminal while developing to rebuild automatically on save.

## Why compiled Tailwind instead of the CDN script

The Tailwind Play CDN (`cdn.tailwindcss.com` / cdnjs equivalent) compiles utility classes live in the browser on every page load. It's explicitly [not recommended for production](https://tailwindcss.com/docs/installation/play-cdn) by the Tailwind team — it's slower, ships every utility class instead of only the ones used, and breaks entirely if the viewing device can't reach the CDN (firewalls, ad-blockers, offline testing). The compiled build in `static/css/public.css` and `static/css/admin.css` works everywhere, every time, with no external dependency at runtime.

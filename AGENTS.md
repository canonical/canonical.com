# AGENTS.md

## Overview

- `canonical.com` is Canonical's Flask-based marketing/site repository.
- The app is server-rendered from `templates/` and `webapp/`, with compiled frontend assets under `static/`.
- The safest local workflow is `dotrun`; CI still also runs direct `yarn` + `python` commands from the repo root.
- Trust the instructions in this file first. Only search the repo if this file is incomplete or you prove one of these instructions is wrong.

## Code layout

- `README.md` - short project overview; confirms `dotrun` is the preferred local workflow.
- `webapp/app.py` - main Flask app, route registration, sitemap/search/navigation wiring, third-party integrations.
- `webapp/application.py` - careers application flow, email sending, Greenhouse/Directory/Calendar integration.
- `webapp/views.py` - shared view helpers, JSON asset helpers, knowledge/event index builders.
- `webapp/navigation.py` - code that reads and shapes navigation data.
- `webapp/greenhouse.py`, `webapp/google_calendar.py`, `webapp/recaptcha.py`, `webapp/marketo.py`, `webapp/partners.py` - external integrations and feature-specific helpers.
- `webapp/canonical_cla/` - Canonical CLA routes/views.
- `templates/` - Jinja templates and markdown-backed page content. Most content-only changes happen here.
- `templates/legal/**/*.md` - markdown source content rendered by the site.
- `templates/knowledge/**/*` - knowledgehub pages.
- `templates/sitemap-index.xml` - top-level sitemap index that links to all section sitemaps.
- `templates/sitemap-links.xml`, `templates/careers/sitemap.xml`, `templates/partners/sitemap.xml`, `templates/knowledge/sitemap.xml`, `templates/data/sitemap.xml` - per-section sitemap templates rendered by routes in `webapp/app.py`.
- `templates/sitemap_tree.xml` - generated (git-ignored) full sitemap; the `/sitemap_tree.xml` route (`build_sitemap_tree` in `webapp/app.py`) regenerates it from the `templates/` tree on a `POST` and serves it on `GET`.
- `templates/llms.txt` - manually maintained LLM-friendly site index (https://llmstxt.org/), committed to git (not generated). Edit this file directly to change what AI crawlers see. Combined with `llms.yaml` at app startup (`webapp/llms.py`, `build_llms_txt`) and served by the `/llms.txt` route (`llms_txt` in `webapp/app.py`).
- `templates/llms-full.txt` - generated (git-ignored) full Markdown content of every renderable page linked from `llms.txt` (`webapp/llms.py`, `build_llms_full_txt`). Pre-generated at build time by `python3 webapp/llms.py generate` (run in the `pack-rock` job of `.github/workflows/deploy.yaml` before `rockcraft pack`); the `/llms-full.txt` route (`llms_full_txt` in `webapp/app.py`) serves it read-only from disk, regenerating on demand only if missing (local dev). Deliberately skips pages served live from Discourse (product docs, tutorials, case studies, events - see `DISCOURSE_PATH_PREFIXES` in `webapp/llms.py`), since the build environment has no Discourse API access and shouldn't scrape and redistribute that content.
- `static/js/` - browser JS/TS entrypoints and React code.
  - `static/js/career-explorer/` - React/TypeScript careers explorer.
  - `static/js/canonical-cla/` - React client for the CLA pages.
  - `static/js/navigation/` and `static/js/*.js` - standalone page behavior modules.
- `static/sass/` - global Sass.
- `build.js` - esbuild bundling for the JS/TS entrypoints.
- `scripts/build-modules.sh` - copies required browser assets from `node_modules` into `static/js/modules/`; `yarn build-js` depends on it.
- `navigation.yaml` - primary navigation data source.
- `secondary-navigation.yaml` - secondary nav/page sidebar data source.
- `redirects.yaml` - redirects config.
- `llms.yaml` - docs-team-owned config for extra curated links inserted into `/llms.txt` right after its "Main pages" section (`heading` + `links`, each with `title`/`url`/`description`), read by `webapp/llms.py`. Must be listed in `rockcraft.yaml` so it ships in the image. Formatting of both this file and `templates/llms.txt` is checked by `yarn lint-llms` (`python3 webapp/llms.py lint`), a required PR check (`lint-llms` job in `.github/workflows/pr.yaml`).
- `tests/` - Python unit tests plus JS/Jest and Playwright tests.
  - `tests/js/` - Jest tests for browser modules.
  - `tests/playwright/` - E2E tests; `tests/playwright/tests/navigation/README.md` explains navigation coverage.
- `package.json` - authoritative list of yarn scripts.
- `requirements.txt` - pinned Python dependencies.
- `.github/workflows/pr.yaml` - the most important CI definition; use it as the source of truth for lint/test/build expectations.
- `.github/workflows/playwright.yaml`, `forms-test.yaml`, `percy-pr.yaml` - specialized browser/form/visual workflows.
- `.github/workflows/sitemap.yaml` - on any `templates/**` push to `main`, POSTs to the live `https://canonical.com/sitemap_tree.xml` endpoint with `SITEMAP_SECRET` to regenerate the git-ignored `templates/sitemap_tree.xml` from the current `templates/` tree.
- `Dockerfile` - production image build.
- `run` - older Docker helper script; works, but README + CI favor `dotrun`.
- `entrypoint` - actual Gunicorn/Talisker server command used by `yarn serve` and container runs.
- `konf/site.yaml` - deployment env vars and staging/production overrides; use this to discover real env names.

## Local development

```bash
dotrun
```

- The site serves successfully at `http://localhost:8002`.
- The first `dotrun` command may take longer than expected because it checks/pulls the dotrun image, creates `.venv`, and installs dependencies.
- For dependency conflicts, it is recommended to run `dotrun clean` first.

Dependencies: Python venv in `.venv/`, Node modules via Yarn.

Copy `.env` values to `.env.local` for local overrides (git-ignored).

## Build

```bash
yarn run build      # Build CSS and JS for production
yarn run build-css  # SCSS → static/css/
yarn run build-js   # TS/JS → static/js/dist/
```

## Testing

```bash
yarn test             # All Python + JS tests with coverage
yarn test-python      # Python unittest + VCR cassettes
yarn test-js          # Jest
yarn test-marketo     # Marketo forms test
yarn test-kh          # Knowledgehub tests
yarn test-e2e         # Playwright end-to-end tests
yarn percy-snapshot   # Visual regression
```

## Linting and formatting

```bash
yarn lint-python      # flake8 + black --check (line-length 79)
yarn lint-scss        # stylelint

yarn format-python    # black --line-length 79
yarn format-prettier  # prettier

djlint templates/path/to/file.html --lint --profile=jinja   # djlint for html/jinja - uses `.djlintrc`
```

## External Service Dependencies

| Service       | Purpose                          | Key Env Vars |
| ------------- | -------------------------------- | ------------ |
| Discourse API | Blog, takeovers, docs, tutorials | `DISCOURSE_API_KEY`, `DISCOURSE_API_USERNAME`, `CHARMHUB_DISCOURSE_API_KEY`, `CHARMHUB_DISCOURSE_API_USERNAME`, `MAAS_DISCOURSE_API_KEY`, `MAAS_DISCOURSE_API_USERNAME` |
| Careers       | Careers related                  | `HARVEST_API_KEY`, `APPLICATION_CRYPTO_SECRET_KEY` |
| Greenhouse    | Candidate applications           | `GREENHOUSE_API_KEY` |
| Google Calendar | Google Calendar service-account auth             | `SERVICE_ACCOUNT_EMAIL`, `SERVICE_ACCOUNT_PRIVATE_KEY` |
| Marketo       | Marketing / lead gen             | `MARKETO_API_URL`, `MARKETO_API_CLIENT`, `MARKETO_API_SECRET` |
| CLA API       | Canonical CLA frontend/backend   | `CANONICAL_CLA_API_URL` |
| reCAPTCHA     | Bot protection                   | `RECAPTCHA_ENABLED`, `RECAPTCHA_SITE_KEY`, `RECAPTCHA_PROJECT_ID`, `RECAPTCHA_API_KEY`, `RECAPTCHA_SCORE_THRESHOLD` |
| Directory API | Directory lookups                | `DIRECTORY_API_TOKEN` |
| SMTP          | Application email sending        | `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_SENDER_ADDRESS` |
| Sitemap       | Sitemap generation               | `SITEMAP_SECRET` |


## Practical tips

- Start with `.github/workflows/pr.yaml` before guessing which checks matter.
- Always run `dotrun` before any dotrun build/lint/test command on a fresh clone.
- Always reinstall Python dependencies after editing `requirements.txt`.
- If you change `templates/*.html`, run `djlint` on the changed file(s).
- If you change navigation behavior or menu content, inspect `navigation.yaml`, `secondary-navigation.yaml`, `webapp/navigation.py`, and the Playwright navigation tests together.
- If you change JS/TS entrypoints, remember `yarn build-js` depends on `scripts/build-modules.sh`.
- If you add or move pages under `templates/`, expect the `sitemap.yaml` workflow to regenerate the sitemap on merge to `main`; update the relevant `templates/**/sitemap*.xml` source when a section's URLs change, and run `tests/test_sitemap.py` to validate.
- Prefer `dotrun` for any task that needs the whole site running.
- Trust this file first; only search when the task falls outside these instructions or the instructions prove incomplete.


## Docs

- `README.md` — project overview, setup, development workflow, and common commands
- `AGENTS.md` — instructions and conventions for AI agents/contributors working in the repository
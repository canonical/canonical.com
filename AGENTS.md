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
- `templates/legal/**/*.md`, `templates/knowledge/**/*.md` - markdown source content rendered by the site.
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
- `tests/` - Python unit tests plus JS/Jest and Playwright tests.
  - `tests/js/` - Jest tests for browser modules.
  - `tests/playwright/` - E2E tests; `tests/playwright/tests/navigation/README.md` explains navigation coverage.
- `package.json` - authoritative list of yarn scripts.
- `requirements.txt` - pinned Python dependencies.
- `.github/workflows/pr.yaml` - the most important CI definition; use it as the source of truth for lint/test/build expectations.
- `.github/workflows/playwright.yaml`, `forms-test.yaml`, `percy-pr.yaml` - specialized browser/form/visual workflows.
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
dotrun test             # All Python + JS tests with coverage
dotrun test-python      # Python unittest + VCR cassettes
dotrun test-js          # Jest
dotrun test-marketo     # Marketo forms test
dotrun test-kh          # Knowledgehub tests
dotrun test-e2e         # Playwright end-to-end tests
dotrun percy-snapshot   # Visual regression
```

## Linting and formatting

```bash
dotrun lint-python      # flake8 + black --check (line-length 79)
dotrun lint-scss        # stylelint

dotrun format-python    # black --line-length 79
dotrun format-prettier  # prettier

djlint templates/path/to/file.html --lint --profile=jinja   # djlint for html/jinja - uses `.djlintrc`
```

## External Service Dependencies

| Service       | Purpose                          | Key Env Vars |
| ------------- | -------------------------------- | ------------ |
| Discourse API | Blog, takeovers, docs, tutorials | `DISCOURSE_API_KEY`, `DISCOURSE_API_USERNAME`, `CHARMHUB_DISCOURSE_API_KEY`, `CHARMHUB_DISCOURSE_API_USERNAME`, `MAAS_DISCOURSE_API_KEY`, `MAAS_DISCOURSE_API_USERNAME` |
| Careers       | Careers related                  | `HARVEST_API_KEY`, `APPLICATION_CRYPTO_SECRET_KEY` |
| Greenhouse    | Candidate applications           | `GREENHOUSE_API_KEY` |
| Google Console | Google console APIs             | `SERVICE_ACCOUNT_EMAIL`, `SERVICE_ACCOUNT_PRIVATE_KEY` |
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
- Prefer `dotrun` for any task that needs the whole site running.
- Trust this file first; only search when the task falls outside these instructions or the instructions prove incomplete.


## Docs

- `README.md` — project overview, setup, development workflow, and common commands
- `AGENTS.md` — instructions and conventions for AI agents/contributors working in the repository
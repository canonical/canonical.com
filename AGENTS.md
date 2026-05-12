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

## Running the code

### Preferred: dotrun

On a fresh clone, this was the most reliable full-stack path:

```bash
yarn install --immutable
python3 -m pip install --user dotrun requests==2.31.0
dotrun install
dotrun build
SECRET_KEY=insecure_test_key \
APPLICATION_CRYPTO_SECRET_KEY=insecure_test_key \
SERVICE_ACCOUNT_EMAIL=test_email@email.com \
SERVICE_ACCOUNT_PRIVATE_KEY=test_private_key \
HARVEST_API_KEY=local_development_fake_key \
RECAPTCHA_SITE_KEY=test \
PORT=8002 \
dotrun
```

- The site serves successfully at `http://127.0.0.1:8002`.
- The first `dotrun` command may take longer than expected because it checks/pulls the dotrun image and creates `.venv`.
- Always run `dotrun install` before the first `dotrun build`/`dotrun` in a fresh clone.

### Direct host commands

These commands were validated successfully from the repo root:

```bash
yarn install --immutable
python3 -m pip install --user -r requirements.txt black==25.1.0 flake8 coverage
yarn build
yarn test-js
yarn lint-scss
yarn lint-python
```

Important caveats from validation:

- `python3 app.py` does **not** start a web server; it only imports `webapp.app`.
- `yarn serve` was **not** reliable in this host environment after ad-hoc installs; it failed with `ModuleNotFoundError: No module named 'zope.event'`.
- If you need to serve the full site locally, prefer `dotrun` over raw `yarn serve`.

### Docker helper

- `./run --help` works and documents the old Docker workflow.
- Use it only if you intentionally want the generated Docker wrapper; otherwise prefer `dotrun`, because that is what README and CI use.

### LLM-related work

- This repo does not contain a checked-in LLM provider/runtime configuration for application features.
- If you add any new LLM configuration, prefer GitHub Models unless the task explicitly requires something else.

## Running the tests

Run these from the repo root.

### Fast checks usually needed for UI/content/code changes

```bash
yarn install --immutable
yarn build
yarn test-js
yarn lint-scss
```

### Python lint

```bash
python3 -m pip install --user -r requirements.txt black==25.1.0 flake8
yarn lint-python
```

### Python tests (CI-style)

Use the same fake secrets CI uses:

```bash
SECRET_KEY=insecure_test_key \
HARVEST_API_KEY=local_development_fake_key \
APPLICATION_CRYPTO_SECRET_KEY=insecure_test_key \
SERVICE_ACCOUNT_EMAIL=test_email@email.com \
SERVICE_ACCOUNT_PRIVATE_KEY=test_private_key \
python3 -m coverage run --source=webapp --omit=webapp/marketo.py -m unittest $(find tests/ -name 'test_*.py' ! -name 'test_marketo.py')
```

Observed behavior:

- In this environment, the first Python test run failed before executing tests because of a system `pyOpenSSL`/Twisted mismatch (`TypeError: deprecated() got an unexpected keyword argument 'name'`).
- This was fixed by running:

```bash
python3 -m pip install --user --upgrade pyOpenSSL
```

- After that fix, the CI-style Python test command passed (`Ran 163 tests ... OK`).

### Jinja lint

CI only lints changed template files:

```bash
python3 -m pip install --user djlint
djlint templates/path/to/file.html --lint --profile=jinja
```

Use `.djlintrc` for style expectations.

### Playwright

- Config is in `playwright.config.ts`.
- Base URL is `http://0.0.0.0:8002`.
- Start the site first with `dotrun`, then run:

```bash
yarn playwright test
```

- Navigation-specific notes are in `tests/playwright/tests/navigation/README.md`.
- Workflow `playwright.yaml` expects `PLAYWRIGHT_USER_ID` and `PLAYWRIGHT_USER_PASSWORD` secrets for some tests.

### Percy / visual tests

- Percy snapshots use `yarn percy-snapshot`.
- Percy workflows rely on `PERCY_TOKEN_WRITE`; local Percy runs need a valid `PERCY_TOKEN`.

### Marketo-only tests

`tests.test_marketo` is not part of the main Python coverage command. The dedicated workflow uses:

```bash
MARKETO_API_URL=https://066-EOV-335.mktorest.com \
MARKETO_API_CLIENT=... \
MARKETO_API_SECRET=... \
python3 -m unittest tests.test_marketo
```

## Upgrading Python dependencies

- There is no lockfile generator here; `requirements.txt` is the source of truth.
- Check candidate versions with:

```bash
python3 -m pip index versions <package>
```

- Then update the pinned line in `requirements.txt`, reinstall, and re-run relevant checks:

```bash
python3 -m pip install --user -r requirements.txt
```

- If you use `dotrun` for development, run `dotrun install` after changing `requirements.txt`.

## ENV

### Common fake local values used successfully here

These are enough for local dotrun smoke tests and for the main CI-style Python test command:

```bash
SECRET_KEY=insecure_test_key
HARVEST_API_KEY=local_development_fake_key
APPLICATION_CRYPTO_SECRET_KEY=insecure_test_key
SERVICE_ACCOUNT_EMAIL=test_email@email.com
SERVICE_ACCOUNT_PRIVATE_KEY=test_private_key
RECAPTCHA_SITE_KEY=test
PORT=8002
```

### Important variables

- `SECRET_KEY` - required by the Flask base app; always set a dummy value locally.
- `PORT` - port used by `yarn serve`/`dotrun`; Playwright and README assume `8002`.
- `HARVEST_API_KEY` - needed for `/careers` work and used in CI as a fake local value.
- `GREENHOUSE_API_KEY` - used by Greenhouse vacancy fetching paths.
- `APPLICATION_CRYPTO_SECRET_KEY` - required by the careers application cipher helpers.
- `SERVICE_ACCOUNT_EMAIL`, `SERVICE_ACCOUNT_PRIVATE_KEY` - used by Google Calendar integration; CI uses fake values.
- `CANONICAL_CLA_API_URL` - CLA frontend/backend endpoint; default deployment values are in `konf/site.yaml`.
- `RECAPTCHA_ENABLED`, `RECAPTCHA_SITE_KEY`, `RECAPTCHA_PROJECT_ID`, `RECAPTCHA_API_KEY`, `RECAPTCHA_SCORE_THRESHOLD` - reCAPTCHA feature flags/config. If `RECAPTCHA_SITE_KEY` is missing, the app logs an error on startup.
- `DIRECTORY_API_TOKEN` - required for employee directory lookups in careers/application flows.
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_SENDER_ADDRESS` - required for application email sending.
- `SEARCH_API_KEY` - custom search integration.
- `DISCOURSE_API_KEY`, `DISCOURSE_API_USERNAME`, `CHARMHUB_DISCOURSE_API_KEY`, `CHARMHUB_DISCOURSE_API_USERNAME`, `MAAS_DISCOURSE_API_KEY`, `MAAS_DISCOURSE_API_USERNAME` - discourse-backed content integrations.
- `MARKETO_API_URL`, `MARKETO_API_CLIENT`, `MARKETO_API_SECRET` - only needed for Marketo tests/integration work.
- `PLAYWRIGHT_USER_ID`, `PLAYWRIGHT_USER_PASSWORD` - only needed for certain Playwright workflows.
- `PERCY_TOKEN` / `PERCY_TOKEN_WRITE` - only needed for Percy snapshot runs.
- `SITEMAP_SECRET` - used by sitemap-related behavior/tests.
- `FLASK_ENV`, `FLASK_DEBUG`, `GREENHOUSE_DEBUG` - environment-mode toggles; see `konf/site.yaml` for staging/demo defaults.

## Practical tips

- Start with `.github/workflows/pr.yaml` before guessing which checks matter.
- Always run `yarn install --immutable` before any yarn build/lint/test command on a fresh clone.
- Always reinstall Python dependencies after editing `requirements.txt`.
- If you change `templates/*.html`, run `djlint` on the changed file(s).
- If you change navigation behavior or menu content, inspect `navigation.yaml`, `secondary-navigation.yaml`, `webapp/navigation.py`, and the Playwright navigation tests together.
- If you change JS/TS entrypoints, remember `yarn build-js` depends on `scripts/build-modules.sh`.
- Prefer `dotrun` for any task that needs the whole site running.
- Trust this file first; only search when the task falls outside these instructions or the instructions prove incomplete.

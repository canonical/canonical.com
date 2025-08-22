# ![Canonical](https://assets.ubuntu.com/v1/efc6527b-CoF%20@2x.png?h=32 "Canonical")&nbsp;canonical.com

**The new codebase, to replace [the old one](https://github.com/canonical-web-and-design/www.canonical.com/).**

[![Code coverage](https://codecov.io/gh/canonical-web-and-design/canonical.com/branch/master/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/canonical.com)

This is the repository for the canonical.com website.

## Architecture overview

This website is written with the help of the [flask](http://flask.pocoo.org/) framework. In order to use functionalities that multiple of our websites here at Canonical share, we import the [base-flask-extension](https://github.com/canonical-web-and-design/canonicalwebteam.flask-base) module.

## Development

The simplest way to run the site is with [the `dotrun` snap](https://github.com/canonical-web-and-design/dotrun/):

```bash
dotrun
```

Afterwards the website will be available at <http://localhost:8002>.

When you start changing files, the server should reload and make the changes available immediately.

## Environment variables

Environment variables are read from the available shell. For the charm, these are prepended with the prefix `FLASK_`, which we strip before re-inserting them into the environment.

## Greenhouse API

To work locally on the `/careers` section of the site, you will need to add a `HARVEST_API_KEY` environment variable to `.env` file. You can find this via the [Greenhouse admin panel](https://canonical.greenhouse.io/configure/dev_center/credentials).

# Deploy

You can find the deployment config in the deploy folder.

# License

The content of this project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/), and the underlying code used to format and display that content is licensed under the [LGPLv3](https://opensource.org/license/lgpl-3-0/) by [Canonical Ltd](http://www.canonical.com/).

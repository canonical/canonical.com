# Repository for the rewrite of canonical.com

This is the repository for the new canonical.com website.

At the moment this is under heavy development and does not relate to any website in production.
To see the site currently running at <https://canonical.com> head to <https://github.com/canonical-web-and-design/www.canonical.com>.

## Architecture overview

This website is written with the help of the [flask](http://flask.pocoo.org/) framework. In order to use functionalities that multiple of our websites here at Canonical share, we import the [base-flask-extension]() module.


## Development

Run `./run` inside the root of the repository and all dependencies will automatically be installed. Afterwards the website will be available at <http://localhost:803XXXX>.
When you start changing files, the server should reload and make the changes available immediately.

### Adding dependencies
This repository is using [poetry](https://poetry.eustace.io/) to manage dependencies.  Refer to its documentation for information on how to install it and user guides.

## Testing

`poetry run pytest` will run all tests in the test directory using [pytest](https://docs.pytest.org/en/latest/).


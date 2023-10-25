# Metadata Catalogue

A Metadata Catalogue

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT


## Setup

First you need to create your secrets

```
cd setup
docker compose up --build
```

This creates the `secrets` directory.


## Development
to setup for development use:
```
pipx install pre-commit
pre-commit install
source helpers.sh
dpcli_dev up --build
```

´helpers.py´ contains a few helpers functions that reduce the boilerplate you need to write to use docker compose cli and django cli.

To run django commands inside the container use, example:
```
djcli_dev migrate
djcli_dev createsuperuser
```

## Production
to test production django container
```
source helpers.sh
dpcli_prod up --build
```

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy metadata_catalogue

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

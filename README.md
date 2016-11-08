# Service Level Objectives Compliance Report

Report on Service Level Objectives Compliance


## Overview

You have a few dashboards in [Librato][] that describe your Service Level
Objectives. You want a report on SLO breaches over the past day/week.

[Librato]: https://librato.com

# Running

## API

    api = sloc_librato.LibratoApi(email=LIBRATO_EMAIL, token=LIBRATO_TOKEN)
        charts = [{'threshold': 100, 'chart_name': 'Website Response Time Mean'}]
        report.daily_report(api, 'SLO - Production Website', charts, 7)

## Command Line

    slocr daily --space 'SLO - Production Website' --chart 'Website Response Time Mean' --threshold 100 --chart 'Website Reponse Time  p95' --threshold 200 --num-days 7

# Developing

## Project Tooling

* [python-project-template][] - Project template and massive timesaver, with many of the below tools prconfigured
* [Paver][] for running miscellaneous tasks
* [Setuptools][] for distribution (Setuptools and Distribute_ have merged_)
* [Sphinx][] for documentation
* [flake8][] for source code checking
* [pytest][] for unit testing
* [mock][] for mocking (not required by the template, but included anyway)
* [tox][] for testing on multiple Python versions


[python-project-template]: https://github.com/seanfisk/python-project-template
[Paver]: http://paver.github.io/paver/
[Setuptools]: https://setuptools.readthedocs.io/en/latest/
[Distribute]: http://pythonhosted.org/distribute/
[Sphinx]: http://sphinx-doc.org/
[flake8]: https://pypi.python.org/pypi/flake8
[pytest]: http://pytest.org/latest/
[mock]: http://www.voidspace.org.uk/python/mock/
[tox]: http://testrun.org/tox/latest/

## Setup with VirtualEnv Et Al

With pyenv and pyenv-virtualenv

    pyenv virtualenv sloc_report
    pyenv local sloc_report

With virtualenvwrapper

    mkvirtualenv sloc_report

   With plain virtualenv_::

    virtualenv VENV
    source VENV/bin/activate

## Install the project's development and runtime requirements

    pip install -r requirements-dev.txt

## Run the unit tests

    paver test

## Run linting

    paver lint

## Run the integration tests

Integration tests require real librato credentials. Ideally this should be a
read-only API token. The following environment variables are required:

* `LIBRATO_EMAIL` - the primary email address associated with the account
* `LIBRATO_TOKEN` - the API token
* `LIBRATO_TEST_SPACE` - Name of a space that exists within the librato account
  and has at least one chart

    paver test_integration

#. Run the tests::

    paver test_all

You should see output similar to this:

    $ paver test_all
    ---> pavement.test_all
    No style errors
    ========================================= test session starts =========================================
    platform darwin -- Python 2.7.3 -- pytest-2.3.4
    collected 5 items

    tests/test_main.py .....

    ====================================== 5 passed in 0.05 seconds =======================================
      ___  _   ___ ___ ___ ___
     | _ \/_\ / __/ __| __|   \
     |  _/ _ \\__ \__ \ _|| |) |
     |_|/_/ \_\___/___/___|___/


# Supported Python Versions

Python Project Template supports the following versions out of the box:

* CPython 2.7, 3.3
* PyPy 1.9

CPython 2.6, and 3.0-3.2 may also work but are at this point unsupported. PyPy
2.0.2 is known to work but is not run on Travis-CI.

Jython_ and IronPython_ may also work, but have not been tested. If there is
interest in support for these alternative implementations, please open a
feature request!

# Licenses

The code which makes up this Python project template is licensed under the
MIT/X11 license. Feel free to use it in your free software/open-source or
proprietary projects.

The template also uses a number of other pieces of software, whose licenses are
listed here for convenience. It is your responsibility to ensure that these
licenses are up-to-date for the version of each tool you are using.

+------------------------+----------------------------------+
|Project                 |License                           |
+========================+==================================+
|Python itself           |Python Software Foundation License|
+------------------------+----------------------------------+
|argparse (now in stdlib)|Python Software Foundation License|
+------------------------+----------------------------------+
|Sphinx                  |Simplified BSD License            |
+------------------------+----------------------------------+
|Paver                   |Modified BSD License              |
+------------------------+----------------------------------+
|colorama                |Modified BSD License              |
+------------------------+----------------------------------+
|flake8                  |MIT/X11 License                   |
+------------------------+----------------------------------+
|mock                    |Modified BSD License              |
+------------------------+----------------------------------+
|pytest                  |MIT/X11 License                   |
+------------------------+----------------------------------+
|tox                     |MIT/X11 License                   |
+------------------------+----------------------------------+

# Issues

Please report any bugs or requests that you have using the GitHub issue tracker!

# Authors

* Richard Clark - <richard@depop.com>
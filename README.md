# `dac`: A CLI Helper Tool for Data as Code

[Data as Code](https://data-as-code.github.io/docs/) (DaC) is a paradigm of distributing versioned data as code.

`dac` is a tool that [supports the Producer](https://data-as-code.github.io/docs/#3-use-the-dac-cli-tool).

**IMPORTANT**: Currently the project is in the initial development phase, this is why releases are marked as `0.z.y`.
(following [semantic versioning 2.0.0](https://semver.org/): "Major version zero (0.y.z) is for initial development.
Anything MAY change at any time. The public API SHOULD NOT be considered stable.").
While in this phase, we will denote breaking changes with a minor increase.

## Quickstart

You can install `dac` as a regular python package

```sh
python -m pip install dac
```

Then use the integrated help to find out its functionalities
```sh
dac --help
```

## Setup development environment (for contributors only)

* Create a virtual environment and activate it

  ```shell
  python -m venv venv
  . venv/bin/activate
  ```

* Install the developer dependencies

  ```shell
  python -m pip install -U pip wheel setuptools
  python -m pip install -r requirements-dev.txt
  ```

* Enable the pre-commits

  ```shell
  pre-commit install
  ```

* To run all the tests

  ```shell
  pytest --run-slow
  ```

  (omit `--run-slow` to run only the fast unit tests)

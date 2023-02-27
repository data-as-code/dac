<div align="center">
  <img src="https://data-as-code.github.io/dac/img/motto.png" width="450"/>
</div>

# `dac`: Data as Code

Data-as-Code (DaC) `dac` is a tool that supports the distribution of data as (python) code.

<div align="center">
  <img src="https://data-as-code.github.io/dac/img/logo.jpg" width="250"/>
</div>

**IMPORTANT**: Currently the project is in the initial development phase, this is why releases are marked as `0.z.y`.
(following [semantic versioning 2.0.0](https://semver.org/): "Major version zero (0.y.z) is for initial development.
Anything MAY change at any time. The public API SHOULD NOT be considered stable.").
While in this phase, we will denote breaking changes with a minor increase.


## 📔 [User documentation](https://data-as-code.github.io/dac/)


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

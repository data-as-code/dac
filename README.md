<div align="center">
  <img src="docs/img/motto.png" alt="drawing" width="450"/>
</div>

# `dac`: Data as Code

Data-as-Code (DaC) `dac` is a tool that supports the distribution of data as (python) code.

<div align="center">
  <img src="docs/img/logo.jpg" alt="drawing" width="250"/>
</div>


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

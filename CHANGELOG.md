# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**IMPORTANT**: Currently the project is in the initial development phase, this is why releases are marked as `0.z.y`.
(following [semantic versioning 2.0.0](https://semver.org/): "Major version zero (0.y.z) is for initial development.
Anything MAY change at any time. The public API SHOULD NOT be considered stable.").
While in this phase, we will denote breaking changes with a minor increase.

## 0.4.1

### Added

* Introduce `dac next-version` command, that allows to find the next minor release for a given python package and (optionally) a given major version.

## 0.4.0

### Changed

* The `load` function in `load.py` can contain optional arguments. Previously no arguments were allowed.
* `load.py` and `schema.py` are publicly accessible under `dac_pkg_name.load` and `dac_pkg_name.schema` respectively. Previously they were marked as private modules, under `dac_pkg_name._load` and `dac_pkg_name._schema`.
* `Schema` does not have to be a `pandera.DataFrameModel` anymore, but any class that implements a `validate` method (see the `_input.interface.Validator` protocol).
* `dac` does not rely on [`pydantic`](https://pypi.org/project/pydantic/) anymore, and uses [`dataclass`](https://docs.python.org/3/library/dataclasses.html#) instead.
  Changes affect `PackConfig` and `PyProjectConfig`.

## 0.3.3

### Fixed

* Cleanup

## 0.3.2

### Changed

* Extend compatibility to pydantic v1. Now `dac` works with both v1 and v2 of pydantic

## 0.3.1

### Changed

* Update code to be compatible with pydantic v2 (no retro-compatibility with v1)

## 0.3.0

### Changed

* Dependencies passed in CLI `--pkg-dependencies` or `PyProjectConfig` must be separated by `;` or newline (previously was `,` or newline)

## 0.2.0

### Added

* First release of `dac`

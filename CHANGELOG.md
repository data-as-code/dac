# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**IMPORTANT**: Currently the project is in the initial development phase, this is why releases are marked as `0.z.y`.
(following [semantic versioning 2.0.0](https://semver.org/): "Major version zero (0.y.z) is for initial development.
Anything MAY change at any time. The public API SHOULD NOT be considered stable.").
While in this phase, we will denote breaking changes with a minor increase.

## 0.3.1

### Changed

* Update code to be compatible with pydantic v2 (no retro-compatibility with v1)

## 0.3.0

### Changed

* Dependencies passed in CLI `--pkg-dependencies` or `PyProjectConfig` must be separated by `;` or newline (previously was `,` or newline)

## 0.2.0

### Added

* First release of `dac`

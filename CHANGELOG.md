# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Features
- GUI for tapipy package [@nathandf](https://github.com/nathandf)

### Breaking Changes
- Router calls index method on BaseController if no command is passed after the resource
- Upgrade tapipy to version 1.0.3

### non-Breaking Changes
- Added CHANGELOG.md
- Added CONTRIBUTORS.md
- select_Action and index methods on TapipyController moved to BaseController
- Prompt util method changed from "not_none" to "text"
- Added prompt util boolean select
- Open API Schema type transform util
- rename core package to utils
- Pacakge create creates Example and Configure controllers
- package settings available on package controllers on instantiation
- Access to settings and config management on the base controller class

### Fixed
- Router: Check if aliases object exists in aliases module before getattr

### Removed
- N/A

## [v1.0.0] - 2021-12-1
### Features
- GUI for tapis package [@nathandf](https://github.com/nathandf)
- Multi-profile support
- Before and After action filters
- Command aliases for packages(except for the tapipy package)
- Base jupyterSCINCO package
.
- Docker deployment option for tapisv3-cli [@nathandf](https://github.com/nathandf) & [@Tyler-Clemens](https://github.com/Tyler-Clemens)

### Breaking Changes
- N/A

### non-Breaking Changes
- N/A

### Fixed
- 

### Removed
- N/A


# Changelog

All notable changes to this project will be documented in this file.

The format is (read: strives to be) based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.1.3] – 2026-02-14
### Fixed:
- Reference core.py and not dworhak_env.py to import DworshakEnv. Fixed in cli.py, cli_stdlib.py, and README.md.

### Internal:
- We need to release and then update dwroshak and dworshak-prompt to fix downstream. References to "item" key are correct.

---

## [0.1.2] – 2026-02-13
### Added:
- core.py
- cli.py content migrated and altered from dworshak-config
- cli_stdlib.py content migrated and altered from dworshak-config

---

## [0.1.1] – 2026-02-13
### Added:
- Publish to PyPI
- Flesh out __init__ to include dworshak_env and DworshakEnv

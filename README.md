
# dworshak-env

[GitHub: dworshak-env](https://github.com/City-of-Memphis-Wastewater/dworshak-env)

`dworshak-env` provides a small, convenient interface for working with environment variables and `.env` files. It is designed to fit into existing workflows without introducing surprises.

This library does **not** replace `os.getenv`. Instead, it helps you manage environment variables in a predictable, Pythonic way and integrates naturally with the broader Dworshak ecosystem:

---

## Installation

```bash
pip install dworshak-env
```

---

## Usage

### Simple access to environment variables

```python
from dworshak_env import DworshakEnv

env = DworshakEnv()
api_url = env.get("API_URL", default="https://api.github.com")
print(api_url)
```

### Loading from a `.env` file

```python
env = DworshakEnv(path=".env")
db_password = env.get("DB_PASSWORD")
```

### Setting defaults

You can instantiate `DworshakEnv` with defaults that act as fallbacks:

```python
defaults = {"API_URL": "https://api.github.com", "DEBUG": "0"}
env = DworshakEnv(defaults=defaults)

print(env.get("API_URL"))  # returns the default if not set in environment
```

---

## Philosophy

`dworshak-env` exists to make environment variables and `.env` files easy to access in Python programs.

It joins the mainstream patterns that Python developers already know, 
while providing smooth prompting to users via DworshakPrompt - because developers are users too.

Use it wherever you want predictable, Pythonic environment variable access, with optional integration into the Dworshak ecosystem.

---

## CLI

The [dworshak](https://github.com/City-of-Memphis-Wastewater/dworshak) layer is the intended primary CLI entry point, but the `dworshak-env` CLI can be used directly.

```bash
pipx install "dworshak-env[typer]"
dworshak-env --version
dworshak-env --help
dworshak-env set "key" 0
```

```
dworshak-env helptree
```

<p align="center">
  <img src="https://raw.githubusercontent.com/City-of-Memphis-Wastewater/dworshak-env/main/assets/dworshak-env_v0.1.6_helptree.svg" width="100%" alt="Screenshot of the dworshak-env CLI helptree">
</p>

`helptree` is utility funtion for Typer CLIs, imported from the `typer-helptree` library.

- GitHub: https://github.com/City-of-Memphis-Wastewater/typer-helptree
- PyPI: https://pypi.org/project/typer-helptree/

---

<a id="sister-project-dworshak-secret"></a>

## Sister Projects in the Dworshak Ecosystem

* **CLI/Orchestrator:** [dworshak](https://github.com/City-of-Memphis-Wastewater/dworshak)
* **Interactive UI:** [dworshak-prompt](https://github.com/City-of-Memphis-Wastewater/dworshak-prompt)
* **Secrets Storage:** [dworshak-secret](https://github.com/City-of-Memphis-Wastewater/dworshak-secret)
* **Plaintext Pathed Configs:** [dworshak-config](https://github.com/City-of-Memphis-Wastewater/dworshak-config)
* **Classic .env Injection:** [dworshak-env](https://github.com/City-of-Memphis-Wastewater/dworshak-env)

```python
pipx install dworshak
pip install dworshak-secret
pip install dworshak-config
pip install dworshak-env
pip install dworshak-prompt

```

---

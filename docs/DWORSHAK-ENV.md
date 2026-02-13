
# Dworshak Env

`dworshak-env` is a lightweight Python library for working with environment variables in a modern, `.env`-friendly way. It bridges the gap between conventional environment management (`os.getenv`) and the Dworshak ecosystem, providing optional interactive prompting for missing values.

It joins the mainstream patterns that Python developers already know, while providing smooth prompting to users via `DworshakPrompt`—because developers are users too.

---

## Key Features

- Access environment variables with a safe Python API.
- Optionally prompt users when a value is missing.
- Supports default values and ephemeral overrides.
- Compatible with `.env` files for familiar workflows.
- Plays nicely with the rest of the Dworshak ecosystem:
  - [`dworshak-prompt`](https://github.com/dworshak/dworshak-prompt)
  - [`dworshak-config`](https://github.com/dworshak/dworshak-config)
  - [`dworshak-secret`](https://github.com/dworshak/dworshak-secret)

`dworshak-env` is not meant to replace `os.getenv`, but it enables developers to integrate prompting and defaults without forcing a new storage paradigm.

---

## Installation

```bash
pip install dworshak-env

Optional: For full Dworshak prompting functionality:

pip install dworshak-prompt


---

Basic Usage

from dworshak_env import DworshakEnv

env = DworshakEnv()

# Get a value from the environment, optionally prompting the user
api_key = env.get("API_KEY", default="default_key")

You can also instantiate DworshakEnv with defaults or fallbacks:

env = DworshakEnv(defaults={"API_KEY": "default_key"})

api_key = env.get("API_KEY")


---

Prompting Missing Values

If a requested environment variable is missing and prompting is enabled, DworshakEnv can interactively ask the user for input via DworshakPrompt.

from dworshak_env import DworshakEnv
from dworshak_prompt import DworshakPrompt

prompt = DworshakPrompt(default_priority=[PromptMode.CONSOLE])

env = DworshakEnv(prompt=prompt)
database_url = env.get("DATABASE_URL")

In CI or non-interactive environments, the default value will be returned.

No surprises: dworshak-env never writes to disk by default.



---

Differentiation from dworshak-config

Feature	dworshak-env	dworshak-config

Storage	Environment variables, .env files	JSON files in ~/.dworshak/
Persistence	Ephemeral, optional overrides	Persistent, structured config
Prompting missing values	Optional with DworshakPrompt	Optional with DworshakPrompt
Hierarchy	Flat key/value	Nested by service/item
Use case	Lightweight, on-ramp, ephemeral	Robust, structured, production-ready


dworshak-env meets developers where they are, while dworshak-config is for structured, persistent storage of configuration values and secrets.


---

CLI Integration (via dworshak)

dworshak-env can be integrated into the Dworshak CLI for interactive prompting:

dworshak env get --key DATABASE_URL

This will:

1. Check the environment variable.


2. If missing, prompt the user via DworshakPrompt.


3. Return the value to your CLI workflow.




---

Philosophy

dworshak-env is not a new cult of configuration. It joins the herd:

Leverages existing Python patterns.

Works seamlessly with .env files.

Provides a gentle on-ramp to the full Dworshak ecosystem (dworshak-config, dworshak-secret, dworshak-prompt).


It’s for developers who want simplicity, safety, and optional user prompting—without committing to a new configuration paradigm.


---

Links

dworshak-prompt – Interactive prompting library.

dworshak-config – Persistent configuration storage.

dworshak-secret – Secure secret storage.




# zephyrex-inventory

Companion app to an ERPNext instance for scanning and tracking parts and assets, built on the Zephyrex framework. ERPNext stays the source of truth; this app is the interface.

Status: skeleton. The server boots with an empty `inventory` extension. There are no models yet, and the client has not been added.

## Layout

```
server/   FastAPI backend, a consumer of the zephyrex Python package
```

A `client/` folder will be added later for the mobile PWA.

## Requirements

- requires-Python = 3.11=<3.14", because the framework crashes on Python 3.14
- Access to GitHub (the framework installs from the ServerFramework repo)

## Running the server

```bash
cd server
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
python app.py
```

The API listens on port 2000. On first boot it creates a SQLite database in the system temp folder (`/tmp/zephyrex_inventory.db`) and seeds it. Two warnings on startup are expected in development: `ROOT_API_KEY` is unset, and `APP_CORS_ALLOWED_ORIGINS` is empty.

To work against a local framework checkout instead, run `pip install -e "../../server-framework[all]"` before the install line above.

## Tests

```bash
cd server
python -m pytest extensions/
```

## Open items

- The framework currently installs from GitHub with no pinned version, so two installs on different days can get different framework code. The plan is to switch to a pinned release.
- The ERPNext bridge is not wired in yet.

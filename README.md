# inventory_scanner

A Frappe app for tracking inventory and assets on ERPNext, with QR code scanning
from a phone. ERPNext is the source of truth. This app adds the scanning and
action screens (receive, move, check in/out, install a part, asset history).

Built for the capstone project. Pushes to `main` that pass the tests deploy to
the shared dev ERP.

## Local setup (Ubuntu 24.04 / WSL)

Frappe v16 needs Python 3.14, Node 24, MariaDB 11.8 and Redis.

1. **Python 3.14:** `uv python install 3.14 --default`
2. **Node 24 and yarn:** install Node with nvm, then `npm install -g yarn`
3. **Redis and build tools:** `sudo apt install -y redis-server pkg-config`
4. **MariaDB 11.8:** Ubuntu 24.04 ships 10.11, so add MariaDB's own repository
   (mariadb.org/download/?t=repo-config, choose Ubuntu "noble", 11.8), then
   `sudo apt install mariadb-server mariadb-client`. Back up any existing
   databases first.
5. **Bench:**
```
   uv tool install frappe-bench
   mkdir -p ~/frappe && cd ~/frappe
   bench init --frappe-branch version-16 --python python3.14 frappe-bench
```
   Keep the bench outside this repo and outside /mnt/c.

## Get the app and create a site (not yet tested, update when someone has)

```
cd ~/frappe/frappe-bench
bench get-app erpnext --branch version-16
bench get-app https://github.com/JamesonRGrieve/zephyrex-inventory --branch main
bench new-site dev.localhost
bench --site dev.localhost install-app erpnext
bench --site dev.localhost install-app inventory_scanner
bench start
```

Then open http://localhost:8000.

## Working on a feature

Branch from `main` (`yourname/feature`), commit, open a pull request, and get one
approval. The pipeline runs ruff and pytest on every push and pull request.

## Conventions

- Prefix anything you create on the shared site with your initials; test data
  uses its own prefix.
- Custom fields and scripts are written into the app's files on the same
  branch as the feature that needs them.

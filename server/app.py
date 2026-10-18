import os
from pathlib import Path
from dotenv import load_dotenv

server_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=server_env_path)

os.environ.setdefault("APP_NAME", "Zephyrex Inventory")
os.environ.setdefault("DATABASE_TYPE", "sqlite")
os.environ.setdefault("DATABASE_NAME", "zephyrex_inventory")
os.environ.setdefault("SEED_DATA", "true")
os.environ.setdefault("JWT_SECRET", "dev-only-change-in-production-32chars!")

from zephyrex import run
EXTENSIONS = "inventory"

def create():
    from zephyrex import instance, set_extensions_root
    set_extensions_root("./extensions")
    
    app = instance(extensions=EXTENSIONS)
    
    from extensions.inventory.router import router as inventory_router
    app.include_router(inventory_router)
    
    return app

if __name__ == "__main__":
    import uvicorn
    app = create()
    uvicorn.run(app, host="0.0.0.0", port=2000)
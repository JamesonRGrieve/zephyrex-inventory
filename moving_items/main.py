import os
from pathlib import Path


def load_dotenv():
	"""Load simple KEY=value entries from a .env file in the working directory."""
	env_file = Path.cwd() / ".env"
	if not env_file.is_file():
		return

	for line in env_file.read_text(encoding="utf-8").splitlines():
		line = line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip().strip("\"'")
		if key:
			os.environ.setdefault(key, value)


load_dotenv()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "dark_team.db"

SECRET_KEY = "chave-temporaria-para-desenvolvimento"
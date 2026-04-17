from os import getenv

__all__ = ["PORT", "IS_PRODUCTION"]

PORT = int(getenv("PORT", "8000")) if getenv("PORT") else 8000

IS_PRODUCTION = getenv("ENVIRONMENT", "development").strip().lower() == "production"
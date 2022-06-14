import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASS = os.getenv("POSTGRES_PASS", "passw0rd")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB   = os.getenv("POSTGRES_DB"  , "database")

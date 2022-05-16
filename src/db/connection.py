from env import (POSTGRES_USER, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)

from sqlalchemy import create_engine

db_url = "postgresql+psycopg2://{USER}@{HOST}:{PORT}/{DB}".format(
    USER=POSTGRES_USER,
    HOST=POSTGRES_HOST,
    PORT=POSTGRES_PORT,
    DB=POSTGRES_DB
)
engine = create_engine(db_url)

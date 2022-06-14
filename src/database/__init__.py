from env import (
    POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

base = declarative_base()
from database.models import user, question

db_url = "postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB}".format(
    USER=POSTGRES_USER,
    PASS=POSTGRES_PASS,
    HOST=POSTGRES_HOST,
    PORT=POSTGRES_PORT,
    DB=POSTGRES_DB
)

engine = create_engine(db_url)

base.metadata.create_all(bind=engine)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from db.tables.user import *
from db.tables.address import *

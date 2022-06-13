from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy import Column
from database import base


class Group(base):
    __tablename__ = "groups"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=40), nullable=False, unique=True)

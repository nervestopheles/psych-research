from sqlalchemy.dialects.postgresql import (UUID, VARCHAR, DATE)
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship

from database import base
from uuid import uuid4


class User(base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    username = Column(VARCHAR(length=50), unique=True)
    password = Column(VARCHAR(length=64))

    group = relationship("Group")
    group_id = Column(UUID(as_uuid=True), ForeignKey(
        "groups.id"), index=True, default=uuid4)

    sex = relationship("Sex")
    sex_id = Column(UUID, ForeignKey("sexs.id"), nullable=True)

    email = Column(VARCHAR(length=320), unique=True, nullable=True)
    phone = Column(VARCHAR(length=15), unique=True, nullable=True)

    first_name = Column(VARCHAR(length=50), nullable=True)
    last_name = Column(VARCHAR(length=50), nullable=True)
    birthday = Column(DATE, nullable=True)

    # completed_tests = relationship("CompletedTests")


class Group(base):
    __tablename__ = "groups"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=40), nullable=False, unique=True)


class Sex(base):
    __tablename__ = "sexs"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=50), unique=True)

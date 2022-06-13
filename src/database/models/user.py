from uuid import uuid4
from sqlalchemy.dialects.postgresql import (UUID, VARCHAR, DATE)
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship

from database import base


class User(base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(VARCHAR(length=50), unique=True)
    password = Column(VARCHAR(length=64))

    group = relationship("Group")
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), index=True, default=uuid4)

    email = Column(VARCHAR(length=320), unique=True, nullable=True)
    phone = Column(VARCHAR(length=15), unique=True, nullable=True)

    first_name = Column(VARCHAR(length=50), nullable=True)
    last_name = Column(VARCHAR(length=50), nullable=True)
    birthday = Column(DATE, nullable=True)

    sex = relationship("Sex")
    sex_id = Column(UUID, ForeignKey("sex.id"), nullable=True)

    # completed_tests = relationship("CompletedTests")


class Sex(base):
    __tablename__ = "sex"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=50), unique=True)
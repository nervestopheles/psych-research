from sqlalchemy.dialects.postgresql import (UUID, VARCHAR, DATE)
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship

from db.schema import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True)
    email = Column(VARCHAR(length=320), unique=True)
    username = Column(VARCHAR(length=50, unique=True))

    first_name = Column(VARCHAR(length=50), nullable=True)
    last_name = Column(VARCHAR(length=50), nullable=True)
    birthday = Column(DATE, nullable=True)

    sex = relationship("Sex")
    sex_id = Column(UUID, ForeignKey("sex.id"), nullable=False)

    completed_tests = relationship("CompletedTests")


class Sex(Base):
    __tablename__ = "test"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=50, unique=True))

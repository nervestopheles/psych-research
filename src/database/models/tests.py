from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TEXT
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import base


class Test(base):
    __tablename__ = "tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(VARCHAR(length=250), unique=True)
    description = Column(TEXT)

    # questoin = relationship("Question")

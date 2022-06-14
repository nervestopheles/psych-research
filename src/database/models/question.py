from sqlalchemy.dialects.postgresql import UUID, TEXT, TIME, INTEGER, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey

from uuid import uuid4
from database import base


class Test(base):
    __tablename__ = "tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(VARCHAR(length=250), unique=True)
    description = Column(TEXT)

    questoin = relationship("Question")
    completed_tests = relationship("CompletedTest")


class Question(base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid4, index=True)
    test_id = Column(UUID(as_uuid=True), ForeignKey(
        "tests.id"), default=uuid4)

    text = Column(TEXT, nullable=False)
    min_time = Column(TIME, nullable=False)

    answers = relationship("ProposedAnswer")


class ProposedAnswer(base):
    __tablename__ = "proposed_answers"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid4, index=True)
    quiestion_id = Column(UUID(as_uuid=True), ForeignKey(
        "questions.id"), default=uuid4)

    text = Column(TEXT, nullable=False)
    score = Column(INTEGER, nullable=False)
    description = Column(TEXT, nullable=True)

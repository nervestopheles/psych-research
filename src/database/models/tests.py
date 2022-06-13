from sqlalchemy.dialects.postgresql import (
    UUID, VARCHAR, DATE, BOOLEAN, TIME, TEXT)
from sqlalchemy import (Column, ForeignKey, Table)
from sqlalchemy.orm import relationship

from database import base


class CompletedTest(base):
    __tablename__ = "completed_test"

    user_id = Column(UUID, ForeignKey("user.id"), primary_key=True)
    test_id = Column(UUID, ForeignKey("test.id"), primary_key=True)

    date = Column(DATE, nullable=False)
    passed = Column(BOOLEAN, nullable=False)
    time = Column(TIME, nullable=False)

    user_answers = relationship("UserAnswers")


class UserAnswer(base):
    __tablename__ = "user_answer"

    question_id = Column(UUID, ForeignKey("question.id"), primary_key=True)

    user_id = Column(UUID, ForeignKey(
        "completed_test.user_id"), primary_key=True)
    test_id = Column(UUID, ForeignKey(
        "completed_test.test_id"), primary_key=True)

    answer = Column(TEXT, nullable=False)
    time = Column(TIME, nullable=False)


questions_test = Table(
    "questions_test",
    base.metadata,
    Column("test_id", ForeignKey("test.id"), primary_key=True),
    Column("question_id", ForeignKey("question.id"), primary_key=True),
)


class Question(base):
    __tablename__ = "question"

    id = Column(UUID, primary_key=True)

    question = Column(TEXT, nullable=False)
    min_time = Column(TIME)

    test = relationship(
        "test", secondary=questions_test, back_populates="question"
    )


class Test(base):
    __tablename__ = "test"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=50))
    description = Column(TEXT)

    question = relationship(
        "question", secondary=questions_test, back_populates="test"
    )

from sqlalchemy.dialects.postgresql import (
    UUID, VARCHAR, BOOLEAN, DATE, TIMESTAMP, TEXT)
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
        "groups.id"), index=True, default=uuid4, nullable=True)

    gender = relationship("Gender")
    gender_id = Column(UUID(as_uuid=True), ForeignKey(
        "genders.id"), nullable=True, default=uuid4)

    email = Column(VARCHAR(length=320), unique=True, nullable=True)
    phone = Column(VARCHAR(length=15), unique=True, nullable=True)

    first_name = Column(VARCHAR(length=50), nullable=True)
    last_name = Column(VARCHAR(length=50), nullable=True)
    birthday = Column(DATE, nullable=True)

    completed_tests = relationship("CompletedTest", cascade="all,delete")


class CompletedTest(base):
    __tablename__ = "completed_tests"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), default=uuid4)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.id"), default=uuid4)
    date = Column(TIMESTAMP, nullable=True)
    passed = Column(BOOLEAN, nullable=True)
    time = Column(TIMESTAMP, nullable=True)

    answers = relationship("UserAnswers", cascade="all,delete")


class UserAnswers(base):
    __tablename__ = "user_answers"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    completed_test_id = Column(UUID(as_uuid=True), ForeignKey(
        "completed_tests.id"), default=uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey(
        "questions.id"), default=uuid4)
    answer = Column(TEXT, nullable=False)
    time = Column(TIMESTAMP, nullable=True)


class Group(base):
    __tablename__ = "groups"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=40), nullable=False, unique=True)


class Gender(base):
    __tablename__ = "genders"

    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR(length=50), unique=True)

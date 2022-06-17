from datetime import datetime, timedelta
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel


class UserAnswerDto(BaseModel):
    id: UUID
    completed_test_id: UUID
    question_id: UUID
    answer: str


class CompletedTestDTO(BaseModel):
    id: UUID
    user_id: UUID
    test_id: UUID
    passed: bool
    date: Optional[datetime]
    time: Optional[timedelta]

    answers: Optional[List[UserAnswerDto]]


class GroupDTO(BaseModel):
    id: UUID
    name: str


class BaseUserDTO(BaseModel):
    id: UUID
    type_id: UUID
    group_id: Optional[UUID]
    username: str

    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]

    completed_tests: Optional[List[CompletedTestDTO]]


class UserDTO(BaseUserDTO):
    password: str

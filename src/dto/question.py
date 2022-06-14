from typing import List, Optional
from pydantic import BaseModel

from uuid import UUID
import datetime


class ProposedAnswerDTO(BaseModel):
    id: UUID
    question_id: UUID
    text: str
    score: int
    description: Optional[str]


class QuestionDTO(BaseModel):
    id: UUID
    test_id: UUID
    text: str
    min_time: Optional[datetime.timedelta]

    answers: Optional[List[ProposedAnswerDTO]]


class TestDTO(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    questions: Optional[List[QuestionDTO]]

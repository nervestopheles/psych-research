import uuid
import datetime

from typing import List
from pydantic import BaseModel


class QuestionDTO(BaseModel):
    id: uuid.UUID
    question: str
    min_time: datetime.timedelta


class TestDTO(BaseModel):
    questions: List[QuestionDTO]

import uuid
import datetime

from typing import List
from pydantic import BaseModel


class Question(BaseModel):
    id: uuid.UUID
    question: str
    min_time: datetime.timedelta


class Test(BaseModel):
    questions: List[Question]


q = [
    Question(
        id=uuid.uuid4(),
        question="Время от времени мне очень хочется выпить, чтобы расслабиться.",
        min_time=datetime.timedelta(seconds=5)),
    Question(
        id=uuid.uuid4(),
        question="В свое свободное время я чаще всего смотрю телевизор.",
        min_time=datetime.timedelta(seconds=5))
]

questions = Test(questions=q)

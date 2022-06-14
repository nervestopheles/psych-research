from sqlalchemy.orm.session import Session
from typing import List, Optional
from uuid import UUID

from dto.question import TestDTO
from database.models.user import User
from database.models.question import Test


def get_tests(user_id: UUID, db: Session) -> List[TestDTO]:
    tests: List[Test] = db.query(Test).filter(User)

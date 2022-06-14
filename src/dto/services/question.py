from sqlalchemy import and_
from sqlalchemy.orm.session import Session
from typing import List, Optional
from uuid import UUID, uuid4

from dto.question import TestDTO
from database.models.user import CompletedTest
from database.models.question import Test


def get_tests(user_id: Optional[UUID], db: Session) -> List[TestDTO]:
    if user_id is None:
        tests: List[Test] = db.query(Test).all()
    else:
        tests: List[Test] = db.query(Test).outerjoin(
            CompletedTest,
            and_(
                CompletedTest.test_id == Test.id,
                CompletedTest.user_id == user_id
            )
        ).filter(
            CompletedTest.id == None
        ).all()

    # TODO: сделать not found exception

    tests_dto: List[TestDTO] = []
    for test in tests:
        test_dto = TestDTO(
            id=test.id,
            name=test.name,
            description=test.description,
            questions=None
        )
        tests_dto.append(test_dto)
    return tests_dto

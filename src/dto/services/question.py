from sqlalchemy import and_
from sqlalchemy.orm.session import Session
from typing import List, Optional
from uuid import UUID, uuid4

from dto.question import ProposedAnswerDTO, QuestionDTO, TestDTO
from database.models.user import CompletedTest
from database.models.question import ProposedAnswer, Question, Test
from dto.services.exception import NotFound


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


def get_test(test_id: UUID, db: Session) -> TestDTO:
    test: Optional[Test] = db.query(Test).filter(
        Test.id == test_id
    ).first()

    if test is None:
        raise NotFound()

    questions: List[Question] = db.query(Question).filter(
        Question.test_id == test_id
    ).all()
    questions_dto: List[QuestionDTO] = []
    for question in questions:

        proposed_answers: List[ProposedAnswer] = db.query(ProposedAnswer).filter(
            ProposedAnswer.quiestion_id == question.id
        ).all()
        proposed_answers_dto: List[ProposedAnswerDTO] = []
        for answ in proposed_answers:

            answ_dto = ProposedAnswerDTO(
                id=answ.id,
                question_id=question.id,
                text=answ.text,
                score=answ.score,
                description=answ.description
            )
            proposed_answers_dto.append(answ_dto)

        question_dto = QuestionDTO(
            id=question.id,
            test_id=question.test_id,
            text=question.text,
            min_time=question.min_time,
            answers=proposed_answers_dto
        )
        questions_dto.append(question_dto)

    test_dto = TestDTO(
        id=test.id,
        name=test.name,
        description=test.description,
        questions=questions_dto
    )
    return test_dto

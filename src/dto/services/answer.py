from sqlalchemy import and_
from sqlalchemy.orm.session import Session
from typing import List, Tuple
from uuid import UUID

from dto.user import CompletedTestDTO
from dto.question import ProposedAnswerDTO, QuestionDTO, TestDTO
from database.models.user import CompletedTest, User, UserAnswers
from database.models.question import ProposedAnswer, Question, Test
from dto.services.exception import TestCompleted, TestNotFound, UserNotFound


def get_questions_for_user(user_id: UUID, test_id: UUID, db: Session) -> Tuple[CompletedTestDTO, List[QuestionDTO]]:

    if db.query(User).filter(User.id == user_id).first() == None:
        raise UserNotFound()
    if db.query(Test).filter(Test.id == test_id).first() == None:
        raise TestNotFound()

    completeds: List[CompletedTest] = db.query(CompletedTest).filter(
        CompletedTest.user_id == user_id,
        CompletedTest.test_id == test_id
    ).all()

    if len(completeds) == 0 or any(completed.passed is None for completed in completeds):
        completed = CompletedTest(
            user_id=user_id,
            test_id=test_id,
            passed=False
        )
        db.add(completed)
        db.flush()
        db.refresh(completed)
        db.commit()

    else:
        if any(completed.passed is True for completed in completeds):
            raise TestCompleted()
        for completed in completeds:
            if completed.passed == False:
                break

    questions: List[Question] = db.query(Question).outerjoin(
        UserAnswers,
        and_(
            UserAnswers.question_id == Question.id,
            UserAnswers.completed_test_id == completed.id
        )
    ).filter(
        Question.test_id == test_id,
        UserAnswers.id == None
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

    return tuple[completed, questions_dto]

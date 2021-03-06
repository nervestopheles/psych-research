import http
from datetime import datetime
from fastapi import status
from sqlalchemy import and_
from sqlalchemy.orm.session import Session
from typing import List, Tuple
from uuid import UUID

from dto.user import CompletedTestDTO, UserAnswerDto
from dto.question import ProposedAnswerDTO, QuestionDTO
from database.models.user import CompletedTest, User, UserAnswers
from database.models.question import ProposedAnswer, Question, Test
from dto.services.exception import AnswerAlreadyRecorded, AnswerNotFound, AnswersNotEnd, NotFound, QuestionNotFound, TestCompleted, TestNotFound, UserNotFound


def get_questions_for_user(user_id: UUID, test_id: UUID, db: Session) -> Tuple[CompletedTestDTO, List[QuestionDTO]]:

    if db.query(User).filter(User.id == user_id).first() == None:
        raise UserNotFound()
    if db.query(Test).filter(Test.id == test_id).first() == None:
        raise TestNotFound()

    completeds: List[CompletedTest] = db.query(CompletedTest).filter(
        CompletedTest.user_id == user_id,
        CompletedTest.test_id == test_id
    ).all()

    if len(completeds) == 0 or all(completed.passed is None for completed in completeds):
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
        UserAnswers.completed_test_id == completed.id
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

    completed_dto: CompletedTestDTO = CompletedTestDTO(
        id=completed.id,
        user_id=completed.user_id,
        test_id=completed.test_id,
        passed=completed.passed,
        date=completed.date,
        time=completed.time
    )

    return (completed_dto, questions_dto)


def confirm_answer(
    completed_test_id: UUID,
    question_id: UUID,
    answer: str,
    db: Session
) -> http.HTTPStatus:

    if db.query(CompletedTest).filter(CompletedTest.id == completed_test_id).first() == None:
        raise TestNotFound()
    if db.query(Question).filter(Question.id == question_id).first() == None:
        raise QuestionNotFound()

    proposed_answer = db.query(ProposedAnswer).filter(
        Question.id == question_id, ProposedAnswer.score == answer).first()
    if proposed_answer == None:
        raise AnswerNotFound()

    if db.query(UserAnswers).filter(
        UserAnswers.question_id == question_id,
        UserAnswers.completed_test_id == completed_test_id
    ).first() != None:
        raise AnswerAlreadyRecorded()

    user_answer: UserAnswers = UserAnswers(
        question_id=question_id,
        completed_test_id=completed_test_id,
        answer=proposed_answer.text
    )
    db.add(user_answer)
    db.flush()
    db.commit()

    return status.HTTP_204_NO_CONTENT


def answer_end(user_id: UUID, test_id: UUID, db: Session) -> http.HTTPStatus:

    questions: Tuple[CompletedTestDTO,
                     List[QuestionDTO]] = get_questions_for_user(user_id, test_id, db)
    if len(questions[1]) == 0:
        db.query(CompletedTest).filter(CompletedTest.id == questions[0].id).update(
            {
                CompletedTest.passed: True,
                CompletedTest.date: datetime.now()
            }
        )
        db.commit()
    else:
        raise AnswersNotEnd()

    return status.HTTP_204_NO_CONTENT


def get_user_answers(user_id: UUID, db: Session) -> List[CompletedTestDTO]:
    tests: List[CompletedTest] = db.query(CompletedTest).filter(
        and_(
            CompletedTest.user_id == user_id,
            CompletedTest.passed == True
        )
    ).all()

    if len(tests) == 0:
        return []

    tests_dto = []
    for test in tests:
        answs: List[UserAnswers] = db.query(UserAnswers).filter(
            UserAnswers.completed_test_id == test.id
        ).all()

        answs_dto = []
        for answ in answs:
            q = db.query(Question).filter(Question.id == answ.question_id).first()
            a = db.query(ProposedAnswer).filter(
                and_(
                    ProposedAnswer.quiestion_id == answ.question_id,
                    ProposedAnswer.text == answ.answer
                )
            ).first()
            answ_dto = UserAnswerDto(
                id=answ.id,
                question=q.text,
                score=a.score,
                completed_test_id=answ.completed_test_id,
                question_id=answ.completed_test_id,
                answer=answ.answer,
            )
            answs_dto.append(answ_dto)

        test_dto = CompletedTestDTO(
            id=test.id,
            user_id=test.user_id,
            test_id=test.test_id,
            passed=test.passed,
            date=test.date,
            answers=answs_dto
        )
        tests_dto.append(test_dto)

    return tests_dto

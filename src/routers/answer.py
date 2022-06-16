import http
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm.session import Session
from typing import List, Tuple
from uuid import UUID

from routers import get_db
from dto.user import CompletedTestDTO
from dto.question import QuestionDTO
from dto.error import BaseError
from dto.services.exception import NotFound, AnswerNotFound, QuestionNotFound, UserNotFound, TestNotFound

import dto.services.answer

router = APIRouter()


@router.get(
    "/questions",
    response_model=Tuple[CompletedTestDTO, List[QuestionDTO]],
    operation_id="getQuestions",
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найдены сущности',
            'model': BaseError
        }
    }
)
async def get_questions_for_user(user_id: UUID, test_id: UUID, db: Session = Depends(get_db)):
    try:
        questions = dto.services.answer.get_questions_for_user(
            user_id, test_id, db)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='NoQuestions', display='Доступные вопросы не найдены.').dict())
    except UserNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='UserNotFound', display='Пользователь не существует.').dict())
    except TestNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='TestNotFound', display='Тест не найден.').dict())
    return questions


@router.post(
    "/answer",
    response_model=http.HTTPStatus,  # status code 204
    operation_id="setAnswer",
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найдены сущности',
            'model': BaseError
        }
    }
)
async def confirm_answer(
    completed_test_id: UUID,
    question_id: UUID,
    answer: str,
    db: Session = Depends(get_db)
):
    try:
        sts = dto.services.answer.confirm_answer(
            completed_test_id, question_id, answer, db)
    except AnswerNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='NoValidAnswer', display='Не существующий ответ.').dict())
    except TestNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='TestNotFound', display='Тест не найден.').dict())
    except QuestionNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='QuestionNotAnswer', display='Вопрос не найден.').dict())
    return sts

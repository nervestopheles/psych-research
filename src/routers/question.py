from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm.session import Session
from typing import List

from routers import get_db
from dto.question import TestDTO
from dto.error import BaseError
from dto.services.exception import NotFound

import dto.services.question

router = APIRouter()


@router.get(
    "/tests",
    response_model=List[TestDTO],
    operation_id="getTests",
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найдены сущности',
            'model': BaseError
        }
    }
)
async def get_tests(db: Session = Depends(get_db)):
    try:
        tests = None  # dto.services.user.get_users(group_id, db)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='NoTests', display='Нет доступных тестов для этого пользователя').dict())
    return tests

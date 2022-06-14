from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from typing import List, Optional
from uuid import UUID

from dto.error import BaseError
from routers import get_db
from dto.user import BaseUserDTO, GroupDTO
import dto.services.user
from dto.services.exception import NotFound

router = APIRouter()


@router.get(
    "/users",
    response_model=List[BaseUserDTO],
    operation_id="getUsers",
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найдены сущности',
            'model': BaseError
        }
    }
)
async def get_users(group_id: Optional[UUID] = None, db: Session = Depends(get_db)):
    try:
        users = dto.services.user.get_users(group_id, db)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='NoUsers', display='Пользователи не найдены.').dict())
    return users


@router.get(
    "/groups",
    response_model=List[GroupDTO],
    operation_id="getGroups",
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Не найдены сущности.',
            'model': BaseError
        }
    }
)
async def get_groups(db: Session = Depends(get_db)):
    try:
        groups = dto.services.user.get_groups(db)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='NoGroups', display='Группы не найдены.').dict())
    return groups

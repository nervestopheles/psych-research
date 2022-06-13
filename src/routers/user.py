from dto.error import BaseError
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from routers import get_db
from dto.user import BaseUser
from database.models.user import User
import services.user

router = APIRouter()


@router.get(
    "/users",
    response_model=List[BaseUser],
    operation_id="getUsers",
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description':'Не найдены сущности',
            'model': BaseError
        }
    }
)
async def get_users(db: Session = Depends(get_db)):
    try:
        users = services.user.get_users(db)
    except services.user.NotFoundUsers:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(
            detail='NoUsers', display='Пользователей не существует').dict())
    return users


@router.post(
    "/user",
    response_model=BaseUser,
    operation_id="createUser",
)
async def create_user(
    name: str,
    passw: str,

    email: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
):
    return None

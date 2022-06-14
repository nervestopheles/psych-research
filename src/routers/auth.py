from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from dto.error import BaseError
from routers import get_db
from dto.user import BaseUserDTO

import dto.services.auth
from dto.services.exception import NotFound

router = APIRouter()

@router.get(
    "/auth",
    response_model=BaseUserDTO,
    operation_id="getUsers",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Не авторизован.',
            'model': BaseError
        }
    }
)
async def get_user_data(username: str, password: str, db: Session = Depends(get_db)):
    try:
        user_data = dto.services.auth.get_user_data(username, password, db)
    except NotFound:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, BaseError(
            detail='Unauthorized', display='Не авторизован.').dict())
    return user_data

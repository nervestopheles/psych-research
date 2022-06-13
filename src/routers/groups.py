from dto.error import BaseError
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from routers import get_db
from dto.groups import GroupDTO
import services.groups


router = APIRouter()


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
        groups = services.groups.get_groups(db)
    except services.groups.NotFoundGroups:
        raise HTTPException(status.HTTP_404_NOT_FOUND, BaseError(detail='NoGroups', display='Группы не найдены.').dict())
    return groups

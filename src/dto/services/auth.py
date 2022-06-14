from typing import Optional
from uuid import uuid4
from sqlalchemy.orm.session import Session
from database.models.user import User
from dto.user import BaseUserDTO
from dto.services.exception import NotFound


def get_user_data(username: str, password: str, db: Session) -> BaseUserDTO:
    user: Optional[User] = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    if user is None:
        raise NotFound()

    user_dto: BaseUserDTO = BaseUserDTO(
        id=user.id,
        type_id=uuid4(),

        username=user.username,
        group_id=user.group_id,

        first_name=user.first_name,
        last_name=user.last_name,

        # completed_tests = db.query(CompletedTest).filter(
        #     CompletedTest.user_id == user.id
        # ).all()
        # if len(completed_tests):
        #     pass
    )
    return user_dto

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm.session import Session
from database.models.user import User
from dto.user import BaseUser


class NotFoundUsers(Exception):
    pass


def get_users(group: Optional[UUID], db: Session) -> List[BaseUser]:
    if group is None:
        users: List[User] = db.query(User).all()
    else:
        users: List[User] = db.query(User).filter(User.group_id == group).all()
    if len(users) <= 0:
        raise NotFoundUsers()

    users_dto: List[BaseUser] = []

    for user in users:
        user_dto: BaseUser = BaseUser(
            id=user.id,
            username=user.username,
            group_id=user.group_id,
            user_type="Student",
        )
        users_dto.append(user_dto)

    return users_dto

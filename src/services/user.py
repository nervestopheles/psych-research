from typing import List
from sqlalchemy.orm.session import Session
from database.models.user import User
from dto.user import BaseUser


class NotFoundUsers(Exception):
    pass


def get_users(db: Session) -> List[BaseUser]:
    users: List[User] = db.query(User).all()
    if len(users) <= 0:
        raise NotFoundUsers()

    users_dto: List[BaseUser] = []

    for user in users:
        user_dto: BaseUser = BaseUser(
            id=user.id,
            username=user.username,
            user_type="Student"
        )
        users_dto.append(user_dto)

    return users_dto

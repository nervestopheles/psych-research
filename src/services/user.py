from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm.session import Session
from database.models.user import User, Group
from dto.user import BaseUserDTO, GroupDTO
from services.exception import NotFound


def get_users(group: Optional[UUID], db: Session) -> List[BaseUserDTO]:
    if group is None:
        users: List[User] = db.query(User).all()
    else:
        users: List[User] = db.query(User).filter(User.group_id == group).all()
    if len(users) <= 0:
        raise NotFound()

    users_dto: List[BaseUserDTO] = []

    for user in users:
        user_dto: BaseUserDTO = BaseUserDTO(
            id=user.id,
            group_id=user.group_id,
            type_id=uuid4(),

            username=user.username,
        )
        users_dto.append(user_dto)

    return users_dto


def get_groups(db: Session) -> List[GroupDTO]:
    groups: List[Group] = db.query(Group).all()
    if len(groups) <= 0:
        raise NotFound()

    groups_dto: List[GroupDTO] = []

    for group in groups:
        group_dto: GroupDTO = GroupDTO(
            id=group.id,
            name=group.name,
        )
        groups_dto.append(group_dto)

    return groups_dto

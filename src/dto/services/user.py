from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm.session import Session
from database.models.user import CompletedTest, User, Group
from dto.user import BaseUserDTO, CompletedTestDTO, GroupDTO
from dto.services.exception import NotFound


def get_users(group_id: Optional[UUID], db: Session) -> List[BaseUserDTO]:
    if group_id is None:
        users: List[User] = db.query(User).all()
    else:
        users: List[User] = db.query(User).filter(
            User.group_id == group_id
        ).all()

    if len(users) <= 0:
        raise NotFound()

    users_dto: List[BaseUserDTO] = []

    for user in users:

        # completed_tests = db.query(CompletedTest).filter(
        #     CompletedTest.user_id == user.id
        # ).all()
        # if len(completed_tests):
        #     pass

        user_dto: BaseUserDTO = BaseUserDTO(
            id=user.id,
            type_id=uuid4(),

            username=user.username,
            group_id=user.group_id,

            first_name=user.first_name,
            last_name=user.last_name,
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

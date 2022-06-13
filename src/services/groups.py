from tokenize import group
from typing import List, Optional
from sqlalchemy.orm.session import Session
from database.models.group import Group
from dto.groups import GroupDTO


class NotFoundGroups(Exception):
    pass


def get_groups(db: Session) -> List[GroupDTO]:
    groups: List[Group] = db.query(Group).all()
    if len(groups) <= 0:
        raise NotFoundGroups()

    groups_dto: List[GroupDTO] = []

    for group in groups:
        group_dto: GroupDTO = GroupDTO(
            id=group.id,
            name=group.name,
        )
        groups_dto.append(group_dto)

    return groups_dto

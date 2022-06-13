from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class BaseUserDTO(BaseModel):
    id: UUID
    type_id: UUID
    group_id: UUID
    username: str

    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]


class UserDTO(BaseUserDTO):
    password: str


class GroupDTO(BaseModel):
    id: UUID
    name: str

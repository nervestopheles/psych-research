from uuid import UUID
from pydantic import BaseModel


class GroupDTO(BaseModel):
    id: UUID
    name: str

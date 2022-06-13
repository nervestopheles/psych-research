from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    id: UUID
    username: str
    user_type: str

    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class User(BaseUser):
    password: str

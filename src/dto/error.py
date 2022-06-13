from typing import List
from pydantic import BaseModel


class BaseError(BaseModel):
    detail: str
    display: str


class BadParametersError(BaseModel):
    class ParameterError(BaseModel):
        name: str
        description: str

    parameters: List[ParameterError]

from pydantic import BaseModel, ConfigDict


class UserIn(BaseModel):
    email: str
    password: str


class User(UserIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    confirmed: bool


class UserLogin(BaseModel):
    email: str
    password: str


class UserConfirmation(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str
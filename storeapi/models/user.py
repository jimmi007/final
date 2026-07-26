from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    email: str


class UserIn(User):
    password: str
<<<<<<< HEAD
# // κληρονομεί το user
=======
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc

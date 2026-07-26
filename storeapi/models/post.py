from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str
<<<<<<< HEAD
    image_url: Optional[str] = None
# optional προαιρετικό
=======

>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc

class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
<<<<<<< HEAD

=======
    image_url: Optional[str] = None
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc


class UserPostWithLikes(UserPost):
    model_config = ConfigDict(from_attributes=True)

    likes: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
<<<<<<< HEAD
# Το from_attributes=True επιτρέπει στην Pydantic να μετατρέπει αντικείμενα
# (π.χ. μοντέλα SQLAlchemy) σε μοντέλα Pydantic διαβάζοντας τα attributes τους αντί να απαιτεί λεξικό (dict).
=======

>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc

class UserPostWithComments(BaseModel):
    post: UserPostWithLikes
    comments: list[Comment]
<<<<<<< HEAD
    # //comments-λιστά με αντικείμενα
=======

>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc

class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    id: int
<<<<<<< HEAD
    user_id: int
=======
    user_id: int
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc

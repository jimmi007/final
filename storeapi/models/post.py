from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str
    image_url: Optional[str] = None
# optional προαιρετικό

class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int



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
# Το from_attributes=True επιτρέπει στην Pydantic να μετατρέπει αντικείμενα
# (π.χ. μοντέλα SQLAlchemy) σε μοντέλα Pydantic διαβάζοντας τα attributes τους αντί να απαιτεί λεξικό (dict).

class UserPostWithComments(BaseModel):
    post: UserPostWithLikes
    comments: list[Comment]
    # //comments-λιστά με αντικείμενα

class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    id: int
    user_id: int
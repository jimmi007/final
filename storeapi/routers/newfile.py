import logging
from enum import Enum
from idlelib import query
from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from storeapi.database import comment_table, database, like_table, post_table, user_table
from storeapi.models.post import (
    Comment,
    CommentIn,
    PostLike,
    PostLikeIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
    UserPostWithLikes,
)
from storeapi.models.user import User
from storeapi.security import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)

async def find_post(search: str):
    logger.info(f"Finding post with string {search}")

    query = post_table.select().where(
        post_table.c.body.ilike(f"%{search}%")
    )

    logger.debug(query)

    return await database.fetch_all(query)

@router.get("/users/posts/count")
async def postsbyuser():
    logger.info(f"Finding posts from user ")
    query = (sqlalchemy.select(
            user_table.c.id,user_table.c.email,
            sqlalchemy.func.count(post_table.c.id).label("count")
            )
            .select_from(user_table.outerjoin(post_table, post_table.c.user_id==user_table.c.id
            ))
            .group_by(user_table.c.id,user_table.c.email)
            )

    logger.debug(query)

    return await database.fetch_all(query)

@router.get("/users/{userid}/posts/count")
async def findtotalposts(userid: int):

    logger.info("Finding posts from user")

    query = (
        sqlalchemy.select(
            user_table.c.id,
            user_table.c.email,
            sqlalchemy.func.count(post_table.c.id).label("post_count")
        )
        .select_from(
            user_table.outerjoin(
                post_table,
                post_table.c.user_id == user_table.c.id
            )
        )
        .where(user_table.c.id == userid)
        .group_by(
            user_table.c.id,
            user_table.c.email
        )
    )

    logger.debug(query)

    return await database.fetch_one(query)

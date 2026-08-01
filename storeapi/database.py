import databases
import sqlalchemy

from storeapi.config import config


metadata = sqlalchemy.MetaData()


user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),

    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, default=False),

)


post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "image_url",
        sqlalchemy.String,
        nullable=True,
    ),
)


comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column(
        "post_id",
        sqlalchemy.ForeignKey("posts.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)


like_table = sqlalchemy.Table(
    "likes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "post_id",
        sqlalchemy.ForeignKey("posts.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)


# SQLite χρειάζεται check_same_thread=False.
# PostgreSQL δεν το χρειάζεται.
if not config.DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing")

connect_args = (
    {"check_same_thread": False}
    if config.DATABASE_URL.startswith("sqlite")
    else {}
)


engine = sqlalchemy.create_engine(
    config.DATABASE_URL,
    connect_args=connect_args,
)


metadata.create_all(engine)


# Μικρό connection pool για PostgreSQL στο Render.
database_options = (
    {"min_size": 1, "max_size": 3}
    if config.DATABASE_URL.startswith("postgres")
    else {}
)


database = databases.Database(
    config.DATABASE_URL,
    force_rollback=config.DB_FORCE_ROLL_BACK,
    **database_options,
)
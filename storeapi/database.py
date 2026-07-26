import databases
import sqlalchemy

from storeapi.config import config

metadata = sqlalchemy.MetaData()
<<<<<<< HEAD
# είναι ένα δοχείο (container) που κρατάει πληροφορίες για όλους τους πίνακες της βάσης
=======

>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
<<<<<<< HEAD
    sqlalchemy.Column("user_id", sqlalchemy.Integer),
    sqlalchemy.Column("image_url", sqlalchemy.String, nullable=True),
)
# Γράφουμε τις στήλες του πίνακα και τι ονόματα έχει..ονομάζουμε το πίνακα post_table
=======
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("image_url", sqlalchemy.String)
)

>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc
user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, default=False)
)


comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False)
)

like_table = sqlalchemy.Table(
    "likes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False)
)

<<<<<<< HEAD
# Μόνο η SQLite χρειάζεται check_same_thread=False
connect_args = (
    {"check_same_thread": False}
    if config.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL,
    connect_args=connect_args,
)

# Επίτρεψε στη βάση(engine) να χρησιμοποιείται από διαφορετικά threads.
#metadata.create_all(engine)

metadata.create_all(engine)
#
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
# Εδώ χρησιμοποιείς τη βιβλιοθήκη databases.Άρα η βάση επιστρέφει στην αρχική κατάσταση.
# metadata.create_all(engine) → δημιουργεί τους πίνακες./Το metadata περιέχει όλα τα tables.
# Χρησιμοποιείται πολύ στα tests με το rollback.database = Database(...) → δημιουργεί το αντικείμενο που θα χρησιμοποιείς μέσα στο FastAPI για όλα τα queries.
=======
if "sqlite" in config.DATABASE_URL:
    engine = sqlalchemy.create_engine(
        config.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = sqlalchemy.create_engine(config.DATABASE_URL)

metadata.create_all(engine)
db_args= {"min_size":1,"max_size":3} if "postgres" in config.DATABASE_URL else {}
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK,**db_args
)
>>>>>>> 30b9f9e64566bd10701d9ee7a8064bc9146992bc

from app.db import DbClient
from app.settings import CONN_STRING


db = DbClient(CONN_STRING)
db.setup_db()
db.insert_dtypes()



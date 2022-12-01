from sqlalchemy import create_engine
from .db_schema import Base


class DbClient:
    def __init__(self):
        self.engine = create_engine('sqlite:///filecheckerdb.db')

    def setup_db(self):
        with self.engine.connect() as conn:
            Base.metadata.create_all(self.engine)
            conn.close()

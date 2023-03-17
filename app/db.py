from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .models import Base, DataType
from .settings import CONN_STRING, DTYPES

class DbClient:
    def __init__(self, conn_string):
        self.engine = create_engine(conn_string)

    def setup_db(self):

        with self.engine.connect() as conn:
            Base.metadata.create_all(self.engine)
            conn.close()


    def insert_dtypes(self):
        with Session(self.engine) as session:
            try:
                existing_dtypes = session.query(DataType)
                existing_dtypes.delete()
                for dtype in DTYPES:
                    dtype_obj = DataType(name=dtype)
                    session.add(dtype_obj)
                session.commit()
            except Exception as e:
                print(f'Exception {e}')
                session.rollback()

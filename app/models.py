from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Column, ForeignKey, Integer, Boolean

Base = declarative_base()


class DataType(Base):
    __tablename__ = 'datatype'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)


class Process(Base):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=32), nullable=False, unique=True)
    file_name = Column(String(length=128))
    file_ext = Column(String(length=4))
    columns = relationship('DataColumn', backref='process_datacolumn')
    # json_file = Column(Integer, ForeignKey('json_file.id'), nullable=True)
    # excel_files = relationship('ExcelFile')


class DataColumn(Base):
    __tablename__ = 'data_column'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('process.id'), nullable=False)
    name = Column(String(length=32), nullable=False)
    dtype_id = Column(Integer, ForeignKey('datatype.id'), nullable=False)
    max_size = Column(Integer, nullable=True, default=0)
    required = Column(Boolean, nullable=False, default=False)
    unique = Column(Boolean, nullable=False, default=False)



class UniqueTogetherColumns(Base):
    __tablename__ = 'unique_together_columns'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('process.id'), nullable=False)
    column_name = Column(String(32), nullable=False)



# class JSONFile(Base):
#     __tablename__ = 'json_file'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(length=64))
#     path = Column(String(length=128))
#     process_id = Column(Integer, ForeignKey('process.id'), nullable=True)
#
#
# class ExcelFile(Base):
#     __tablename__ = 'excel_file'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(length=64))
#     path = Column(String(length=128))
#     process_id = Column(Integer, ForeignKey('process.id'), nullable=True)

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Column, ForeignKey, Integer

Base = declarative_base()



class Process(Base):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=32))
    json_file = Column(Integer, ForeignKey('json_file.id'), nullable=True)
    excel_files = relationship('ExcelFile')


class JSONFile(Base):
    __tablename__ = 'json_file'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=64))
    path = Column(String(length=128))
    process_id = Column(Integer, ForeignKey('process.id'), nullable=True)


class ExcelFile(Base):
    __tablename__ = 'excel_file'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=64))
    path = Column(String(length=128))
    process_id = Column(Integer, ForeignKey('process.id'), nullable=True)

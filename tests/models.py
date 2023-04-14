from sqlalchemy import Column, Integer, String
from tests.conftest import Base


class Instance(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

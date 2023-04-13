from sqlalchemy import Column, Integer, String
from tests.conftest import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

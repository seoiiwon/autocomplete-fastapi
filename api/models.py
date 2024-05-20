from sqlalchemy import *
from config.database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
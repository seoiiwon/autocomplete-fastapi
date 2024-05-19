import datetime
from pydantic import BaseModel, field_validator

class Post(BaseModel):
    id : int
    subject : str
    content : str
    date : datetime.datetime 
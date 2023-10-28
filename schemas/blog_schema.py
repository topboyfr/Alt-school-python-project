from pydantic import BaseModel
from datetime import date


class BlogCreate(BaseModel):
    title: str
    body: str
    # author: str

class BlogUpdate(BlogCreate):
    pass

class blogDisplay(BlogCreate):
    date_posted: date

    class Config:
        orm_mode = True
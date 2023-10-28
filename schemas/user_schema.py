from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    fullname: str
    
class UserCreate(UserBase):
    email: str = "user@user.com"
    password: str



from sqlalchemy import Column, Integer, String, Date, Date, ForeignKey
import database
from sqlalchemy.orm import relationship


class Blog(database.Base):
    __tablename__ = 'blogs'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String, nullable= False)
    body = Column(String, nullable= False)
    date_posted = Column(Date, nullable= False)
    author = Column(String, nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates = "blogs")

class User(database.Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String, nullable= False)
    fullname = Column(String, nullable= False)
    email = Column(String, nullable= False)
    password = Column(String, nullable= False)

    blogs = relationship("Blog", back_populates = "owner")

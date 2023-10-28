from typing import Generator
from jose import jwt
from fastapi import HTTPException, status
import database
from models import User


SECRET_KEY = "topboysupersecretkey"
ALGORITHM = "HS256"

class functions:
    
    @staticmethod
    def get_db() -> Generator:
        try:
            db = database.SessionLocal()
            yield db
        finally:
            db.close()
    
    def decode_token(db, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms =[ALGORITHM])
            username:str = payload.get("sub") #"sub" is a field holding the username/email address
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid Email credentials")
            
            user = db.query(User).filter(User.email==username).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="User is not authorized")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unable to verify credentials")
        
        #return the user as authenticated
        return user
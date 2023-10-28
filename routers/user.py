from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user_schema import UserBase, UserCreate
from sqlalchemy.orm import Session
from services import app_service
from models import User
from jose import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login_token")


SECRET_KEY = "topboysupersecretkey"
ALGORITHM = "HS256"

user_router = APIRouter()

@user_router.post("/login_token")
def retrieve_token_after_authentication(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(app_service.functions.get_db)):

    auth_user = db.query(User).all()
    
    for row in auth_user:
        if row.email == form_data.username and row.password == form_data.password:
            data = {'sub': form_data.username}
            jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": jwt_token, "token_type": "bearer"}
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Wrong credentials"
        )

#view all existing users
@user_router.get("/view_users")
def view_users(db:Session=Depends(app_service.functions.get_db)):
    all_users = db.query(User).all()
    return all_users

@user_router.post("/create_user")
async def add_user(my_user: UserCreate, db:Session=Depends(app_service.functions.get_db)):
    emails = db.query(User).all()
    for row in emails:
        if row.email == my_user.email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already in use")
        if row.username == my_user.username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="username already in use, Try another nickname")
    
    new_user = User(
        username=my_user.username,
        fullname=my_user.fullname,
        email = my_user.email,
        password = my_user.password,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return my_user
    # raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=my_user)

#EDITING USER INFORMATION BY User ONLY
@user_router.put("/update/{id}")
async def edit_user_profile(id:int, new_updates:UserBase, db:Session = Depends(app_service.functions.get_db), token:str=Depends(oauth2_scheme)):
    
    auth_user = app_service.functions.decode_token(db, token)

    check_user = db.query(User).filter(User.id==id)
    if not check_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    if check_user.first().id == auth_user.id:

        check_user.update(new_updates.__dict__ )                    #Alternatively
        db.commit()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Updated successfully')
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'contact the owner')


@user_router.delete("/delete/{id}")
async def delete_user_profile(id: int, db:Session = Depends(app_service.functions.get_db), token:str=Depends(oauth2_scheme)):
    
    auth_user = app_service.functions.decode_token(db, token)

    user = db.query(User).filter(User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    if user.first().id == auth_user.id:
    
        user.delete()
        db.commit()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="deleted successfully")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'contact the owner')

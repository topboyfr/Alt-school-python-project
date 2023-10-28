from fastapi import APIRouter, Depends, HTTPException, status
from schemas.blog_schema import BlogCreate, BlogUpdate, blogDisplay
from sqlalchemy.orm import Session
from services import app_service
from models import Blog
from datetime import datetime
from routers.user import oauth2_scheme


SECRET_KEY = "topboysupersecretkey"
ALGORITHM = "HS256"

blog_router = APIRouter()

#view all blog
@blog_router.get('/view/all')
async def view_blogs(db:Session=Depends(app_service.functions.get_db)):
    blogs = db.query(Blog).all()
    return blogs

@blog_router.get("/view/{id}", response_model= list[blogDisplay], )  
async def get_blog_by_id(id:int, db:Session=Depends(app_service.functions.get_db)):
    blog = db.query(Blog).filter(Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='article not found')
    print('found')
    return blog
# HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= blog)


@blog_router.post("/create_blog")
async def add_blog(my_blog:BlogCreate, db:Session=Depends(app_service.functions.get_db), token:str=Depends(oauth2_scheme)):
    
    auth_user = app_service.functions.decode_token(db, token)

    new_blog = Blog(**my_blog.dict(), date_posted = datetime.now().date(), owner_id = auth_user.id, author = auth_user.fullname)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail='Blog created successfully')    

#EDITING AN ARTICLE BY Author ONLY
@blog_router.put("/update/{id}")
async def update_blog(id:int, my_blog:BlogUpdate, db:Session=Depends(app_service.functions.get_db), token:str=Depends(oauth2_scheme)):
    
    auth_user = app_service.functions.decode_token(db, token)
    
    search_blog_id = db.query(Blog).filter(Blog.id==id)
    if not search_blog_id.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")
    
    if search_blog_id.first().owner_id == auth_user.id:
        search_blog_id.update(my_blog.__dict__ )
    
        db.commit()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Book updated successfully')
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'contact the owner')



@blog_router.delete("/delete/{id}")
async def delete_blog_profile(id: int, db:Session = Depends(app_service.functions.get_db), token:str=Depends(oauth2_scheme)):
    
    auth_user = app_service.functions.decode_token(db, token)
    
    blog = db.query(Blog).filter(Blog.id==id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog does not exist")
            
    
    if blog.first().owner_id == auth_user.id:

        blog.delete()
        db.commit()
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="deleted successfully")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'contact the owner')

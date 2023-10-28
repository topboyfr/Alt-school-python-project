from fastapi import FastAPI
from routers import blog 
from routers import user 
import database

database.Base.metadata.create_all(bind = database.engine)

app = FastAPI()

app.include_router(blog.blog_router, prefix="/blogs", tags=["Blogs"])
app.include_router(user.user_router, prefix="/users", tags=["Users"])



@app.get("/")
def home():
    return {"Welcome to my blog Application"}

# @app.get("/about")
# def about():
#     return {"About us"}

# @app.post("/login")
# async def login(
#     username: Annotated[str, Form()],
#     password: Annotated[str, Form()],
#     email: Annotated[str, Form()]
# ):
#     print(username, password, email)
#     return {"username": username}


from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends ,status ,Response,HTTPException
import schemas ,models,hashing,database
from database import engine , SessionLocal ,get_db
from typing import List,Optional
from hashing import Hash
from sqlalchemy.orm import relationship
# from .routers import blog

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# app.include_router(blog.router)


def get_db(): 
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get_db = database.get_db()

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blog'])
def destroy(id,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {id} not found')
    
    db.delete(synchronize_session=False)
    db.commit()
    return "done"

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
def update(id,request:schemas.Blog,db :Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Blog with id {id} not found')

    blog.update(request)
    db.commit() 
    return 'update'

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blog'])
def create(request:schemas.Blog,db :Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog 


# @app.get('/blog',response_model=List[schemas.ShowBlog],tags=['blog'])
# def all(db :Session=Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

@app.get('/blog/{id}',status_code = 200 ,response_model=schemas.ShowBlog,tags=['blog'])
def show(id,response:Response,db :Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail= f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f"Blog with the id {id} is not available"}

    return blog 


@app.post('/user',response_model=schemas.ShowUser,tags=['user'])
def create_user(request:schemas.User,db :Session=Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 


@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['user'])
def get_user(id:int,db :Session=Depends(get_db)):
    user =db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail= f"User with the id {id} is not available")
    return user

@app.get('/user_all',response_model=List[schemas.ShowUser],tags=['user'])
def get_user(db :Session=Depends(get_db)):
    user =db.query(models.User).all()

    return user
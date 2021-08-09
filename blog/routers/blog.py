from typing import List
from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session
import schemas,database,models,oauth2
from database import get_db
from repository import blog


router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/{id}',status_code = 200 ,response_model=schemas.ShowBlog)
def show(id,db :Session=Depends(get_db)):
    return blog.show(id,db) 

@router.get('/',response_model=List[schemas.ShowBlog])
def get_all(db :Session=Depends(database.get_db),get_current_user:schemas.User=Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session=Depends(get_db)):
    return destroy(id,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog,db :Session=Depends(get_db)):
    return update(id,request,db)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db :Session=Depends(get_db)):
    return blog.create(request,db)
from sqlalchemy.orm import Session,relationship
from fastapi import Depends ,APIRouter
from .. import models , schemas
from .. import database
from typing import List,Optional

router = APIRouter()



@router.get('/blog',response_model=List[schemas.ShowBlog],tags=['blog'])
def all(db :Session=Depends(database.get_db())):
    blogs = db.query(models.Blog).all()
    return blogs
import sys

from sqlalchemy.sql.functions import user
sys.path.append(r"D:\fastapi\blog")
from fastapi import APIRouter , Depends ,HTTPException,status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
import schemas,models,JWTtoken
from database import get_db
from hashing import Hash 
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invalid Credentials")

    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    #generate a jwt token and return 
    access_token = JWTtoken.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
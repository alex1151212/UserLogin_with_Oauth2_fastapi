import sys
sys.path.append(r"D:\fastapi\blog")
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends ,status ,Response,HTTPException
import schemas ,models,hashing,database
from database import engine ,get_db ,SessionLocal
from typing import List,Optional
from hashing import Hash
from sqlalchemy.orm import relationships
from routers import blog,user,authentication

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)



    
if __name__ == "__main__":
    for i in sys.path:
        print(i)
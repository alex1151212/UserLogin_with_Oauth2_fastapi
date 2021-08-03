from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title:str
    body:str

    
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str 
    password:str

    class Config():
        orm_mode = True
    
class Blog(BlogBase):
    title:str
    body:str
  
class ShowUser(BaseModel):
    name:str
    email:str 
    blogs:List[Blog] = []

    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title:str 
    body:str
    creator:ShowUser

    class Config():
        orm_mode = True
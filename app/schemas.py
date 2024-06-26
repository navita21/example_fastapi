from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    name:str
    age:int
    city:str

class UserOut(BaseModel):
    id:int
    email: EmailStr
    class Config:
        orm_mode=True



class PostCreate(PostBase):
    pass

class Post(BaseModel):
    name:str
    age:int
    city:str
    owner_id: int
    owner:UserOut
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str


    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    dir: int 

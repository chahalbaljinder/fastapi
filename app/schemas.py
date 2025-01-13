from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True        #Here True is default value for publication

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    #other fields are inherited from PostBase reduce redundancy

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    

class UserResponse(UserBase):
    id: int
    created_at: datetime
    #other fields are inherited from PostBase reduce redundancy
    class Config:
        orm_mode = True

class Userlogin(BaseModel):
    email: EmailStr
    password: str

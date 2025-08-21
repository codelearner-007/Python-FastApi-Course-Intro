from pydantic import BaseModel ,EmailStr  # This is for importing the base model
from datetime import datetime

class PostBase(BaseModel):
    title: str  # it define the types of data received from front end
    content: str
    published: bool = True  # It comes with default condition as "True"

class PostCreate(PostBase):
   pass

class Post(PostBase):
    id : int
    created_at : datetime
    
    class Config:
        orm_mode = True


# .................................................................

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email : EmailStr
    
    class Config:
        orm_mode = True
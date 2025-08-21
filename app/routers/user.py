from .. import models, schemas, utils
from fastapi import FastAPI, status, HTTPException, Response, Depends ,APIRouter
from typing import Optional , List
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter()

# .................................................................................
# ........................ get method for All User Data ...........................

@router.get('/users', response_model=list[schemas.UserOut])
def get_user(db : Session = Depends(get_db)):
    users =  db.query(models.User).all()

    return users

# .................................................................................
# .......................... post method for User .............................


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    print(user)
    print(user.dict())
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# .................................................................................
# .......................... get method for Single User .............................

@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int , db : Session = Depends(get_db)):
    user =  db.query(models.User).filter(models.User.id == id).first()
   
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"User with id {id} does not exist")
    
    return user

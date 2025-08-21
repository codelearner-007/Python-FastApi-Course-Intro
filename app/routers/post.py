from .. import models, schemas, utils
from fastapi import FastAPI, status, HTTPException, Response, Depends ,APIRouter
from typing import Optional , List
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter()

# .................................................................................
# .......................... get function for posts .............................


@router.get("/posts", response_model=list[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# .................................................................................
# .......................... post method for post .............................


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# .......................... get method for latest post .............................
# .................................................................................


@router.get("/posts/latest", response_model=schemas.Post)
def get_latest_post(db:Session = Depends(get_db)):
    latest_post = (db.query(models.Post).order_by(models.Post.created_at.desc()).first())
   
    return latest_post


# .................................................................................
# .......................... get method for specific post  .......................

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


# .................................................................................
# .......................... delete method for specific post .......................


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# .................................................................................
# .......................... update method for specific post .......................



@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate , db: Session = Depends(get_db)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    # my_post[index] get the old post replace it with new post "post_dict"
    return post_query.first()


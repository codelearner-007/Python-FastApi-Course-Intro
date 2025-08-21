from typing import Optional , List
from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from random import randrange  # This is for the random number used in id
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models , schemas , utils
from .database import engine, get_db
from .models import User

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# This is the base model for the Post Request



while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', user='postgres', password='090078601@Ab', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)

# This we make a my_post data array for every now post we make from front end
my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "favirot food", "content": "I like pizza", "id": 2}]


# This is the "find product" function having argument of "id"
def find_post(id):
    for post in my_post:
        if post['id'] == id:
            return post

#  Here we find the "index" of the delete post id


def find_index_post(id):
    for i, post in enumerate(my_post):
        if post['id'] == id:
            return i


@app.get("/")
def home():
    return {"message": "Hello World"}


# .................................................................................
# .......................... get function for post .............................


@app.get("/posts", response_model=list[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# .................................................................................
# .......................... post method for post .............................


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# .......................... get method for latest post .............................
# .................................................................................


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_post[len(my_post)-1]
    return latest_post


# .................................................................................
# .......................... get method for specific post  .......................

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


# .................................................................................
# .......................... delete method for specific post .......................


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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



@app.put("/posts/{id}", response_model=schemas.Post)
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


# .................................................................................
# .................................................................................
# ..........................********** USER DATA ********** .......................
# .................................................................................
# .................................................................................

# .................................................................................
# .......................... post method for post .............................


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    print(user)
    print(user.dict())
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


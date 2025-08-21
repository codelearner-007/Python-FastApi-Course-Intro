from typing import Optional , List
from fastapi import FastAPI, status, HTTPException, Response, Depends 
from random import randrange  # This is for the random number used in id
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models , schemas , utils
from .database import engine, get_db
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
 

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

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "Hello World"}


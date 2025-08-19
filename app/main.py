from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel  # This is for importing the base model
from typing import Optional
from random import randrange  # This is for the random number used in id
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# This is the base model for the Post Request


class Post(BaseModel):
    title: str  # it define the types of data received from front end
    content: str
    published: bool = True  # It comes with default condition as "True"


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

# Here we get all the post available in the array


@app.get("/posts")
def get_post():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


# In that case the model do not have the "id" in it and we create the id for the every post which we create
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s , %s ,%s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_post[len(my_post)-1]
    return {"detail": latest_post}


# ///////////////////////////////////////////
# Get Post by ID:
@app.get("/posts/{id}")  # This is for the URL
def get_post(id: int):  # we get the id is parameter like "2" and validate it as string now if the id is not a integer entered by the user then it shows that the id is not a integer other wise it gives the generic error
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    # Lets suppose We don't have the post which the user want then
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post Detail":  post}

# Special NOte
# Any time we have a path parameter like "@app.get("/posts/{id}")"  its result is always be a string like in this case there is a "2" but this is a string type
# we have to manually convert it into a integer so that we can get the 2 post


# ---- This is the delete case -----#
# In this we find the index of the post which we want to delete. If index not found then it means that the post is not there. but if found the my_post.pop(index) will remove the post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post

    cursor.execute(
        """ DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---- This is the Update case -----#
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")

    # my_post[index] get the old post replace it with new post "post_dict"
    return {"data": updated_post}

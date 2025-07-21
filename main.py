from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel  # This is for importing the base model
from typing import Optional
from random import randrange  # This is for the random number used in id

app = FastAPI()

# This is the base model for the Post Request


class Post(BaseModel):
    title: str  # it define the types of data received from front end
    content: str
    published: bool = True  # It comes with default condition as "True"
    rating: Optional[int] = None
    # Optional as if it is present, it only be a integer other wise it will be none
    id: Optional[int] = None


# This we make a my_post data array for every now post we make from front end
my_post = [{"title": "title of post 1",
            "content": "content of post 1", "id": 1}, {"title": "favirot food", "content": "I like pizza", "id": 2}]


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/posts")
def get_post():
    return {'data': my_post}


@app.post("/posts")
def create_posts(post: Post):
    # post_dict = post.dict()
    post.id = randrange(0, 10000000)
    my_post.append(post)
    return {'data': post}

# @app.post("/posts")
# def create_posts(post: Post):
#     post_dict = post.dict()
#     post_dict["id"] = randrange(0, 10000000)
#     my_post.append(post_dict)
#     return {'data': post_dict}

from fastapi import FastAPI, Response, status, HTTPException
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
    # id: Optional[int] = None


# This we make a my_post data array for every now post we make from front end
my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "favirot food", "content": "I like pizza", "id": 2}]


# This is the "find product" function having argument of "id"
def find_post(id):
    for post in my_post:
        if post['id'] == id:
            return post


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/posts")
def get_post():
    return {'data': my_post}


# In that case the model do not have the "id" in it and we create the id for the every post which we create
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_post.append(post_dict)
    # return {'data': post_dict}
    return {'Message ': "New post created"}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_post[len(my_post)-1]
    return {"detail": latest_post}


# ///////////////////////////////////////////
# Get Post by ID:
@app.get("/posts/{id}")  # This is for the URL
def get_post(id: int, response: Response):  # we get the id is parameter like "2" and validate it as string now if the id is not a integer entered by the user thn it shows that the id is not a integer other wise it gives the generic error

    # We find the product using the "id" received and save it into a new variable "post"
    print(type(id))  # Here in print it show that type of id is a string type
    post = find_post(id)  # NOW HERE THE type is integer

    # Lets suppose We don't have the post which the user want then
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"post Detail":  post}

# Special NOte
# Any time we have a path parameter like "@app.get("/posts/{id}")"  its result is always be a string like in this case there is a "2" but this is a string type
# we have to manually convert it into a integer so that we can get the 2 post

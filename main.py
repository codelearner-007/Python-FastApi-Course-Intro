from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_post():
    return {'data': "This is your posts"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print("payload", payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}

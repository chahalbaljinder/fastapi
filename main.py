from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

my_posts = [{"title": "post1", "content": "content1", "id":1}, {"title": "post2", "content": "content2", "id":2}]

app=FastAPI()


class Post(BaseModel):
    title: str
    content: str 
    publish: bool = True  #Here True is default value for publish
    rating: Optional[int] = None  #Here rating is an optional field 
    
@app.get("/")  #decorator (/ is the path such as /login , /home , etc.)
async def root():
    return {"message": "Hello World!!"} #it can be anything like a dictonary, string, etc.


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": f"title: {payload['title']} content: {payload['content']}"}


#using pydantic library for schema 
@app.post("/newpost")
def create_post(new_post: Post):
    '''print(new_post)                   #all content
    print(new_post.title)  #specific field '''
    post_dict = new_post.model_dump()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)  #to have a dictionary view of data
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}  #returning the last post


@app.get("/posts/{id}")
def get_post(id: int):
    post = my_posts[id-1]
    return {"data": post}


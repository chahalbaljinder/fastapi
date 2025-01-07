from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .config import host, database, user, password

app=FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    publish: bool = True  #Here True is default value for publish
    rating: Optional[int] = None  #Here rating is an optional field 

while True:
    try:
        connection = psycopg2.connect(host=host,
                                      database=database,
                                user=user,
                                password=password,
                                cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Connected to the database")

        break

    except Exception as e:
        print("connection failed")
        print("error:",e)
        time.sleep(2)

my_posts = [{"title": "post1", "content": "content1", "id":1}, {"title": "post2", "content": "content2", "id":2}]

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}  #returning the last post


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = my_posts[id-1]
    return {"data": post}


#using pydantic library for schema 
@app.post("/newpost" , status_code=201)
def create_post(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)  #to have a dictionary view of data
    return {"data": my_posts}


@app.delete("/posts/{id}", status_code=204) #status code 204 means no content is sent back to show deleted content
def delete_post(id: int):
    post = my_posts.pop(id-1)
    return {"data": {f"post with id {id} is deleted": post}}


@app.put("/posts/{id}")
def update_post(id: int, new_post: Post):
    my_posts[id-1] = new_post.model_dump()
    return {"data": my_posts}


@app.patch("/posts/{id}")
def update_post(id: int, new_post: Post):
    my_posts[id-1] = new_post.model_dump()
    return {"data": my_posts}



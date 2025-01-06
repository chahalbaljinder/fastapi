from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from app.config import host, database, user, password

app=FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True  #Here True is default value for publish
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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}  #returning the last post


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    post = cursor.fetchone()
    return {"data": post}


#using pydantic library for schema 
@app.post("/newpost" , status_code=201)
def create_post(new_post: Post):
    try:
        cursor.execute(
            "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
            (new_post.title, new_post.content, new_post.published))
        new_post = cursor.fetchone()    #fetch the newly created post
        connection.commit()  #commit the changes to the database
        return {"data": new_post}
    except Exception as e:
        # Rollback in case of an error
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.delete("/posts/{id}", status_code=204) #status code 204 means no content is sent back to show deleted content
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *" ,(str(id)))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found")
    else:
        return {"data": {f"post with id {id} is deleted": deleted_post}}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, str(id)))
    updated_posts = cursor.fetchone()
    connection.commit()

    if updated_posts == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found")
    else:
        return {"data": updated_posts}


@app.patch("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s WHERE id = %s RETURNING *", (post.title, str(id)))
    updated_posts = cursor.fetchone()
    connection.commit()
    
    if updated_posts == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found") 
    else:
        return {"data": updated_posts}



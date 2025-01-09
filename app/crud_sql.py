from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from fastapi import Depends
from .config import host, database, user, password
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True        #Here True is default value for publication

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


@app.get("/posts")
def get_posts(db: Session =Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/sqlalchemy")
def test_posts(db: Session =Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
    


@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session =Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() #filter the post by id
    if post == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found")
    else:
        return {"data": post}


#using pydantic library for schema 
@app.post("/newpost" , status_code=201)
def create_post(new_post: Post,db: Session =Depends(get_db)):
    try:
        # cursor.execute(
        #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        #     (new_post.title, new_post.content, new_post.published))
        # new_post = cursor.fetchone()    #fetch the newly created post
        # connection.commit()  #commit the changes to the database

        #new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
        new_post=models.Post(**new_post.dict())    #**new_post.dict() is used to convert the pydantic model to dictionary
        db.add(new_post) #add the new post to the database
        db.commit()  #commit the changes to the database
        db.refresh(new_post)  #refresh the database to get the newly created post
        return {"data": new_post}
    except Exception as e:
        # Rollback in case of an error
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.delete("/posts/{id}", status_code=204) #status code 204 means no content is sent back to show deleted content
def delete_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *" ,(str(id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False) #delete the post by id & 
                                                                                                        #synchronize_session=False is used to avoid the error
    db.commit()

    if deleted_post == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found")
    else:
        return {"data": {f"post with id {id} is deleted": deleted_post}}


@app.put("/posts/{id}")
def update_post(id: int, post: Post,db:Session =Depends(get_db)):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, str(id)))
    # updated_posts = cursor.fetchone()
    # connection.commit()
    updated_posts = db.query(models.Post).filter(models.Post.id == id).update(post.dict(), synchronize_session=False)

    if updated_posts == 0:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found")
    else:
        db.commit()
        updated_post = db.query(models.Post).filter(models.Post.id == id).first()
        return {"data": updated_post}
    
    
@app.patch("/posts/{id}")
def update_post(id: int, post: Post,db:Session =Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s WHERE id = %s RETURNING *", (post.title, str(id)))
    # updated_posts = cursor.fetchone()
    # connection.commit()
    updated_posts = db.query(models.Post).filter(models.Post.id == id).update(post.dict(), synchronize_session=False)
    
    
    if updated_posts == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found") 
    else:
        db.commit()
        updated_posts = db.query(models.Post).filter(models.Post.id == id).first()
        return {"data": updated_posts}
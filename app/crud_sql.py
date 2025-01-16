from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from . import utils
import time
from sqlalchemy.orm import Session
from fastapi import Depends
from .config import host, database, user, password
from . import models,schemas
from .database import engine, get_db
from app.routers import post, User, auth 

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

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

app.include_router(post.router)
app.include_router(User.router)
app.include_router(auth.router)
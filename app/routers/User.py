from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Users"]
)

@router.post("/logusers", status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.user(**user.dict())

    # hash the password
    hashed_password = utils.hash_password(user.password)
    # assign the hashed password to the user
    new_user.password = hashed_password
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.user).all()
    return users

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"user with id {id} not found")
    return user
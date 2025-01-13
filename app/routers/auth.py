from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=200)
def login(user_credentials:schemas.Userlogin, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == user_credentials.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    return {"token": "example token"}
    
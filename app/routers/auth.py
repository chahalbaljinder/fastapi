from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, Oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=200, response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.user).filter(models.user.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    access_token = Oauth2.create_access_token(data={"user_id": user.email}) #create access token

    return {"access_token": access_token, "token_type": "bearer"}
    
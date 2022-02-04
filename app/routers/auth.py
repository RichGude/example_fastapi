# For generating user and administrative token credentials

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # The OAuthForm has only two fields, 'username' and 'password', and no other fields
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # Verify that the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    # Verify that the login password matches the user password - maintain a consistent HTTP status
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    # Create and return token
    access_token = oauth2.create_access_token(data = { "user_id": user.id })
    return { 'access_token': access_token, "token_type": "bearer" }


from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, Depends, HTTPException
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

#SECRET KEY
# ALGORITHM
#EXPIRATION TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode= data.copy()

    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token( token : str, credentials_exception):
    #print("it is",token)
    try:
    
        payload= jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id:str = str(payload.get("user_id"))
        #print("id is",id)
        #print("This is",payload)

        if id is None:
            raise credentials_exception
        token_data= schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data    
    
def get_current_user(token : str= Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Couldnot validate credentials", 
                                        headers={"WWW-authenticate":"Bearer"})
    
    return verify_access_token(token, credentials_exception)

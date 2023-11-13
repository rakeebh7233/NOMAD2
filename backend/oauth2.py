from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import access_tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return access_tokens.verify_token(token, credentials_exception)
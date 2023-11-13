from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import json


SECRET_KEY = "9ada8cc76f42770d493eea65201cd3d07cf88215328ea6c59bb417739360815c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

with open("users.json", "r") as json_file:
    users = json.load(json_file)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None 

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserData(BaseModel):
    username: str 
    full_name: str or None = None
    email: str or None = None
    hashed_password: str
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_usernames(user_list: dict):
    usernames = []
    for user in user_list:
        usernames.append(user.lower())
    return usernames

def get_user(user_list: dict, username: str):
    usernames = get_usernames(users)
    if username.lower() in usernames:
        user_data = user_list[username]
        return UserInDB(**user_data)

def authenticate_user(user_list: dict, username: str, password: str):
    user = get_user(user_list, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False 
    return user 

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user(users, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(curret_user: UserInDB = Depends(get_current_user)):
    if curret_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return curret_user

# pwd = get_password_hash("16521117")
# print(pwd)
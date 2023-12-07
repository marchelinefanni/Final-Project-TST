from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.auth import *
import json


SECRET_KEY = "9ada8cc76f42770d493eea65201cd3d07cf88215328ea6c59bb417739360815c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

with open("data/users.json", "r") as json_file:
    users = json.load(json_file)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

auth_router = APIRouter(tags=['Authentication'])

# AUTHENTICATION FUNCTIONS
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


# AUTHENTICATION API
@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

'''
# REGISTER
@app.post('/register')
async def register(user: User, password: str):
    user_dict = user.dict()
    user_found = False 
    for u in users:
        if user.username == u:
            user_found = True 
            return "Username " + str(user.username) + " exists."
    if not user_found:
        new_user = UserData()
        new_user.username = user.username
        new_user.full_name = user.full_name
        new_user.email = user.email
        new_user.hashed_password = get_password_hash(password)
        new_user.disabled = False
        new_user_data = vars(new_user)
        users[user.username] = new_user_data
        with open("users.json","w") as write_file9:
            json.dump(users, write_file9, indent=2)
        return new_user_data 
    raise HTTPException(
        status_code=404, detail=f'USER NOT FOUND'
    )
'''

@auth_router.get("/users/me/", response_model=User)
async def read_current_user_info(current_user: User = Depends(get_current_active_user)):
    return current_user

@auth_router.get("/users/me/items")
async def read_current_user_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]
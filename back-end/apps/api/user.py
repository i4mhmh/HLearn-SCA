import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import model, db
from passlib.context import CryptContext
from typing import Union
from typing_extensions import Annotated
from datetime import datetime, timedelta, timezone
import settings


userRouter = APIRouter(
    prefix="/api/user",
    tags=["User"]
)


@userRouter.get('/create')
def root():
    model.Base.metadata.create_all(bind=db.engine)
    return {"create table success"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class sign_in_User(BaseModel):
    username: str
    passwd: str
    fullname: str


class loginUser(BaseModel):
    username: str
    passwd: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


def verify_password(plaintext_passwd, hashed_passwd):
    return pwd_context.verify(plaintext_passwd, hashed_passwd)


def get_password_hash(password):
    return pwd_context.hash(password)


# 注册
@userRouter.post("/sign_in")
async def user_register(user: sign_in_User):
    try:
        hashed_passwd = get_password_hash(user.passwd)
        userInfo = model.User(username=user.username, passwd=hashed_passwd, fullname=user.fullname)
        dbs = db.SessionLocal()
        dbs.add(userInfo)
        dbs.commit()
        dbs.refresh(userInfo)
        return JSONResponse({
            'code': 200,
            'msg': "注册成功",
        })
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="注册失败",
        )

# 登录

## 创建token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=(600))
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


## 验证密码
def authenticate_user(username: str, passwd: str):
    dbs = db.SessionLocal()
    userInfo = dbs.query(model.User).filter(model.User.username == username).first()
    try:
        if verify_password(passwd, userInfo.passwd):
            return userInfo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username or password is wrong",
            headers={"WWW-Authenticate": "Bearer"},
        )


@userRouter.post("/login")
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate cerdentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# Token 验证

## 获取用户
def get_user(username: str):
    dbs = db.SessionLocal()
    try:
        userInfo = dbs.query(model.User).filter(model.User.username == username).first()
        if userInfo is not None:
            return userInfo
    except:
        return False
    return False


# 验证token
@userRouter.get("/verify-token")
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username)
    return user.fullname
# 退出登录

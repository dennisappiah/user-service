from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from ..models import Users
from ..dtos.authdto import CreateUserResponse, CreateUserRequest, Token
from ..utils.db_dependency import get_db
from ..utils.auth_dependency import create_access_token
from ..utils.passwordhash import get_hash_password, password_verify

router = APIRouter(prefix="/auth", tags=["auth"])

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: db_dependency):
    # get user with the username
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not password_verify(password, user.hashed_password):
        return False

    return user


@router.post(
    "/register",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(db: db_dependency, user_request: CreateUserRequest):
    # Check if the username or email already exists
    db_user = (
        db.query(Users)
        .filter(
            (Users.username == user_request.username)
            | (Users.email == user_request.email)
        )
        .first()
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )
    new_user = Users(
        email=user_request.email,
        username=user_request.username,
        firstname=user_request.first_name,
        lastname=user_request.last_name,
        hashed_password=get_hash_password(user_request.password),
        role=user_request.role,
        is_active=True,
    )

    db.add(new_user)
    db.commit()

    response_data = CreateUserResponse(
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.firstname,
        last_name=new_user.lastname,
        role=new_user.role,
    )

    return response_data


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )

    access_token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )

    return {"access_token": access_token, "token_type": "bearer"}

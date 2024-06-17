from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from ..utils.db_dependency import get_db
from ..utils.auth_dependency import get_current_user
from ..utils.passwordhash import get_hash_password, password_verify
from ..dtos.userverificationdto import UserVerification
from ..models import Users

router = APIRouter(prefix="/user", tags=["user"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not password_verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = get_hash_password(user_verification.new_password)

    db.add(user_model)
    db.commit()

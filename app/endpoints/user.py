from app import schemas
from app import crud
from app import models
from app.auth.services import generate_token
from app.helpers.db import get_db
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/login', description='Sign-in.', response_model=schemas.Token)
def login_for_access_token(authenticate: schemas.UserAuthSchema, db: Session = Depends(get_db)):
    access_token = generate_token(db=db, email=authenticate.email, password=authenticate.password)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/", response_model=schemas.UserResponseSchema)
def create_user(user_in: schemas.UserCreateSchema,
                db: Session = Depends(get_db)):
    if user := crud.user.get_by_email(db=db, email=user_in.email):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f'Already exists a user with email {user.email}')
    try:
        return crud.user.create(db=db, obj_in=user_in)
    except HTTPException:
        # raise Exception(e) from e
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail='Has been occurred a problem trying create the user.')


@router.put('/{user_id}',
            response_model=schemas.UserResponseSchema)
def update_user(user_id: int,
                user_in: schemas.UserUpdateSchema,
                db: Session = Depends(get_db)):
    if user_obj := crud.user.get(db=db, id=user_id):
        try:
            user_updated = crud.user.update(db=db, obj_in=user_in, db_obj=user_obj)
            return schemas.UserResponseSchema(**user_updated.__dict__)
        except HTTPException:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                 detail='Has been occurred a problem trying create the user.')
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f'User {user_id} does not exist.')


@router.get('/',
            response_model=list[schemas.UserResponseSchema])
def get_users(db: Session = Depends(get_db)):
    if users := crud.user.get_multi(db=db):
        return users
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail='No se encontraron usuarios.')


@router.get('/{user_id}',
            response_model=schemas.UserResponseSchema)
def get_user(user_id: int,
             db: Session = Depends(get_db)) -> dict | Any:
    if user := crud.user.get(id=user_id, db=db):
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='No existe el usuario.')


user_router = router

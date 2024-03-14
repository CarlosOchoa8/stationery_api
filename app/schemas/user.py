from typing import Any

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, model_validator, field_validator, Field, ConfigDict
from app.auth.services import validate_password


class UserBaseSchema(BaseModel):
    first_name: str = Field(min_length=5, max_length=30)
    last_name: str = Field(min_length=5, max_length=30)
    email: EmailStr = Field(examples=["email@some.com"])
    phone_number: str

    @field_validator('first_name', 'last_name')
    def std_name(cls, value: Any) -> BaseModel:
        value = value.capitalize()
        return value.strip()

    @field_validator('phone_number')
    def stp_phone(cls, value: Any) -> BaseModel:
        return value.strip()


class UserCreateSchema(UserBaseSchema):
    password: str
    re_password: str

    @model_validator(mode="after")
    def validate_passwords(cls, values):
        password = values.password
        re_password = values.re_password
        if password != re_password:
            raise HTTPException(
                detail="Passwords do not match.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not validate_password(password):
            raise HTTPException(
                status_code=400,
                detail="La contraseña debe tener de 5 a 10 caracteres, 1 letra mayúscula, 1 letra minúscula, 1 número, "
                       "1 signo (! @ # $ % & * . _) y no debe contener espacios",
            )

        return values


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None


class UserResponseSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class UserAuthSchema(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    # token_type: str = 'bearer'

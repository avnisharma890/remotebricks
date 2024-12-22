from pydantic import BaseModel, EmailStr
# from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class User(BaseModel):
    id: str
    email: EmailStr
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ExternalID(BaseModel):
    external_id: str

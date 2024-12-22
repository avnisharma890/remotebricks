from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from app.models.models import UserCreate, User, Token, ExternalID
from app.config.database import db
from app.auth import (
    verify_password, get_password_hash,
    create_access_token, get_current_user
)

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    if  db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email Already Registered")
    
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    result =  db.users.insert_one(user_dict)

    return {**user_dict, "id": str(result.inserted_id)}


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/link-id")
async def link_id(
    external_id: ExternalID,
    current_user: dict = Depends(get_current_user)
):
    user = db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    db.user_ids.insert_one({
        "user_id": user["_id"],
        "external_id": external_id.external_id
    })
    return {"message": "ID linked successfully"}


@router.get("/user-data")
async def get_user_data(current_user: dict = Depends(get_current_user)):
    pipeline = [
        {"$match": {"email": current_user["email"]}},
        {
            "$lookup": {
                "from": "user_ids",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "linked_ids"
            }
        }
    ]
    result =  list(db.users.aggregate(pipeline))
    if not result:
        raise HTTPException(status_code=404, detail="User Not Found")
    return result[0]


@router.delete("/user")
async def delete_user(current_user: dict = Depends(get_current_user)):
    user = db.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    # delete chaining to first delete linked ids and then user
    db.user_ids.delete_many({"user_id": user["_id"]})
    db.users.delete_one({"_id": user["_id"]})

    return {"message": "User and related data deleted successfully"}
from fastapi import APIRouter,HTTPException,status
from fastapi.encoders import jsonable_encoder
import secrets

from ..schemas import User,db
from ..hashing.Hash import hasher,verify

router = APIRouter(tags=["users"])

@router.post("/registration",response_description="User Registration")
async def registration(user:User):
    user = jsonable_encoder(user)
    user_found = await db["users"].find_one({"name":user.name})
    email_found = await db["users"].find_one({"name":user.email})
    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User Already Registered")
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email Already Registered")

    user["password"] = hasher(user["password"])
    user["apiKey"] = secrets.token_hex(30)

    new_user = await db["users"].insert_one(user)
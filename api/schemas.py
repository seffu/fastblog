import motor.motor_asyncio
from dotenv import load_dotenv
from bson import ObjectId
from pydantic import BaseModel,Field,EmailStr
import os
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))

db = client.skn

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate 
    @classmethod
    def validate(cls,v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls,field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id:PyObjectId = Field(default_factory=PyObjectId,alias="_id")
    name:str = Field(...)
    email:EmailStr = Field(...)
    password:str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectID:str}
        schema_extra = {
            "example":{
                "name":"John Doe",
                "email":"johndoe@domain.com",
                "password":"secret_code"
            }
        }
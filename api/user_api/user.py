from typing import Optional
from fastapi import APIRouter, HTTPException
from database.userservice import *
from pydantic import BaseModel
import re

user_router = APIRouter(prefix="/user", tags=["Customers/Users"])

regex = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

def check_email(email):
    if re.fullmatch(regex, email):
        return True
    return False

class User(BaseModel):
    id: int
    username: str
    phone: str
    email: str
    user_city: Optional[str] = None
    address: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


@user_router.post("/register_user")
async def register_user_api(user_id: int, username:str, phone: str, email:str, city = None, address=None):
    new_user = reg_user_db(user_id = id,username=username,phone=phone, email=email,city=city,address=address)
    mail_validation = check_email(new_user.email)
    if mail_validation:
        result = reg_user_db(reg_user_db)
        return result, {"status": 1, "messages": "Successfully registered"}
    return {"status": 0, "messages": "Error"}


@user_router.post("/exact_user")
async def get_exact_user_api(user_id: str):
    result = get_exact_user_db(user_id)
    return result

@user_router.get("/get_all_users")
async def get_all_users_api():
    return get_all_users_db()

@user_router.get("/get_update_users")
async def get_update_user_api(user_id:int, change_info: str, new_info: str):
    result = update_user_db(user_id, change_info, new_info)
    return result
@user_router.get("/by_email/{email}", response_model=User)
async def get_user_by_email_api(email: str):
    result = email
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    return result


@user_router.delete("/delete_profile")
async def delete_profile_api(user_id: int):
    result = delete_user_db(user_id)
    return result
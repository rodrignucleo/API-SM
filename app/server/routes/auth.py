from fastapi import APIRouter, HTTPException
from server.auth.auth_handler import check_password, sign_jwt, hash_pass
from server.models.token_model import TokenModel, UserLoginModel
from server.database import user_collection
from server.models.user import UserSchema
from server.database import user_collection

router = APIRouter()

@router.post("/login", response_description="Login user")
async def user_login(user: UserLoginModel):
    # get user from db by e-mail
    result = await user_collection.find_one({"email": user.username})
    # check if password valid and user is active
    if result and check_password(result["password"], user.password):
        # creating jwt by user id
        token: TokenModel = sign_jwt(str(result["_id"]))
        return token
    raise HTTPException(status_code=404, detail="not found")

@router.post("/register", response_description="Register user")
async def create_user(userRequest: UserSchema):
    user_hashed: UserSchema = UserSchema(
        name = userRequest.name,
        email = userRequest.email,
        password = hash_pass(userRequest.password),
        projects = userRequest.projects
    ) 
    result = await user_collection.insert_one(user_hashed.model_dump())
    if result:
        token: TokenModel = sign_jwt(str(result.inserted_id))
        return token
    else:
        raise HTTPException(status_code=400, detail="bad request")
    
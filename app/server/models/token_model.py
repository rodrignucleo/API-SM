from pydantic import BaseModel

class TokenModel(BaseModel):
    access_token: str
    
class UserLoginModel(BaseModel):
    username: str 
    password: str
    
    
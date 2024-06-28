import time
from typing import Dict
import bcrypt
from decouple import config
import jwt

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

salt = bcrypt.gensalt()

def token_response(token: str):
    return {
        "access_token": token
    }

# create jwt from id and stamp
def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 30000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

# checks if token is expired
def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

# get user id from token
async def get_user_id_from_token(token: str) -> str:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token["user_id"]
    except:
        return None

def hash_pass(password: str):
    return bcrypt.hashpw(
        password=bytes(password, 'utf-8'),
        salt=salt
    ).decode('utf-8')

def check_password(hashed_pass: str, user_password: str):
    check = bcrypt.checkpw(
        password=bytes(user_password,'UTF-8'),
        hashed_password=bytes(hashed_pass,'UTF-8')
    )

    if check:
        return True
    else:
        return False
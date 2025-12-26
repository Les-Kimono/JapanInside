from fastapi import FastAPI, Request, HTTPException, status
import utils
import utils.jwt_utils

app = FastAPI()

def check_login(request: Request) -> bool:
    auth_payload = request.headers.get("Authorization")
    if not auth_payload:
        return False
    try:
        auth_token = auth_payload.split(" ")[1]
        utils.jwt_utils.decode_token(auth_token)
        return True
    except (IndexError, utils.jwt_utils.JwtError):
        return False

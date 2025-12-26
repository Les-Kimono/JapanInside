from fastapi import FastAPI, HTTPException, APIRouter, Request, status
from pydantic import BaseModel
import hashlib
import utils.jwt_utils  

app = FastAPI()
router = APIRouter()

class LoginPayload(BaseModel):
    password: str

EXPECTED_HASH =  b'=y\xd7yN\x0b\x01\x17\xe0\x00\xd1\xe3\x03\xact\xdc'

@router.post("/login")
async def login(payload: LoginPayload):
    tried_password = payload.password.encode("utf-8")
    hashed = hashlib.md5(tried_password).digest()

    if hashed == EXPECTED_HASH:
        token = utils.jwt_utils.build_token()
        return {"success": True, "admin": True, "token": token, "message": "Connexion réussie"}
    else:
        raise HTTPException(status_code=401, detail="ncorrect password")

@router.post("/verify-token")
async def verify_token(request: Request):
    if utils.login_utils.check_login(request):
        return {"message": "Ok"}
    else:
        raise HTTPException(status_code=401, detail="Access token isn't well formed")
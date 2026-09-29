import hashlib, hmac, os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, Request
from app.config import settings
from app.database import get_user_by_id

def hash_password(password):
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"

def verify_password(password, stored):
    try:
        _, salt, digest = stored.split("$", 2)
        actual = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, bytes.fromhex(digest))
    except (ValueError, TypeError):
        return False

def create_access_token(user_id):
    now = datetime.now(timezone.utc)
    return jwt.encode({
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.access_token_minutes)).timestamp())
    }, settings.secret_key, algorithm="HS256")

def decode_access_token(token):
    try:
        return int(jwt.decode(token, settings.secret_key, algorithms=["HS256"])["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(401, "Invalid or expired token")

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(401, "Authentication required")
    user = get_user_by_id(decode_access_token(token))
    if not user:
        raise HTTPException(401, "User not found")
    return user

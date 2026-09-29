from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import RedirectResponse
from app.auth import hash_password, verify_password, create_access_token
from app.database import create_user, get_user_by_email

router=APIRouter()

def cookie(resp, token):
    resp.set_cookie("access_token",token,httponly=True,samesite="lax",secure=False,max_age=3600)

@router.post("/register")
def register(email:str=Form(...),password:str=Form(...)):
    if len(password)<8: raise HTTPException(400,"Password must be at least 8 characters")
    if get_user_by_email(email): raise HTTPException(409,"Account already exists")
    uid=create_user(email,hash_password(password))
    resp=RedirectResponse("/dashboard",303); cookie(resp,create_access_token(uid)); return resp

@router.post("/login")
def login(email:str=Form(...),password:str=Form(...)):
    u=get_user_by_email(email)
    if not u or not verify_password(password,u["password_hash"]):
        raise HTTPException(401,"Invalid email or password")
    resp=RedirectResponse("/dashboard",303); cookie(resp,create_access_token(u["id"])); return resp

@router.post("/token")
def token(email:str=Form(...),password:str=Form(...)):
    u=get_user_by_email(email)
    if not u or not verify_password(password,u["password_hash"]): raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_access_token(u["id"]),"token_type":"bearer"}

@router.get("/logout")
def logout():
    resp=RedirectResponse("/",303); resp.delete_cookie("access_token"); return resp

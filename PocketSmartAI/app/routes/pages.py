from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.auth import get_current_user
from app.database import list_history
import json

router=APIRouter()
templates=Jinja2Templates(directory="app/templates")

def maybe_user(request):
    try: return get_current_user(request)
    except Exception: return None

@router.get("/")
def index(request:Request): return templates.TemplateResponse(request,"index.html",{"user":maybe_user(request)})
@router.get("/login")
def login_page(request:Request): return templates.TemplateResponse(request,"login.html",{"user":maybe_user(request)})
@router.get("/register")
def register_page(request:Request): return templates.TemplateResponse(request,"register.html",{"user":maybe_user(request)})
@router.get("/dashboard")
def dashboard(request:Request):
    u=get_current_user(request); return templates.TemplateResponse(request,"dashboard.html",{"user":u,"history":list_history(u["id"])[:6]})
@router.get("/home-planner")
def home_page(request:Request):
    u=get_current_user(request); return templates.TemplateResponse(request,"home_planner.html",{"user":u})
@router.get("/party-planner")
def party_page(request:Request):
    u=get_current_user(request); return templates.TemplateResponse(request,"party_planner.html",{"user":u})
@router.get("/jewelry-planner")
def jewelry_page(request:Request):
    u=get_current_user(request); return templates.TemplateResponse(request,"jewelry_planner.html",{"user":u})
@router.get("/history")
def history_page(request:Request):
    u=get_current_user(request); records=[]
    for r in list_history(u["id"]):
        records.append({"id":r["id"],"planner_type":r["planner_type"],"created_at":r["created_at"],
                        "request":json.loads(r["request_json"]),"response":json.loads(r["response_json"])})
    return templates.TemplateResponse(request,"history.html",{"user":u,"records":records})

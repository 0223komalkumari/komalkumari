from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db, list_history, get_recommendation
from app.auth import get_current_user
from app.routes.auth import router as auth_router
from app.routes.planners import router as planner_router
from app.routes.pages import router as page_router
import json

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app=FastAPI(title=settings.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.allowed_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(page_router); app.include_router(auth_router); app.include_router(planner_router)

@app.get("/health")
def health(): return {"status":"ok","app":settings.app_name,"gemini_configured":bool(settings.gemini_api_key)}

@app.get("/session-info")
def session_info(user=Depends(get_current_user)): return {"authenticated":True,"user_id":user["id"],"email":user["email"]}

@app.get("/session-data")
def session_data(user=Depends(get_current_user)): return {"user_id":user["id"],"email":user["email"],"message":"Session is active."}

@app.get("/history")
def history_api(user=Depends(get_current_user)):
    return [{"id":r["id"],"planner_type":r["planner_type"],"created_at":r["created_at"],
             "request":json.loads(r["request_json"]),"response":json.loads(r["response_json"])}
            for r in list_history(user["id"])]

@app.get("/recommendations-details/{history_id}")
def details(history_id:int,user=Depends(get_current_user)):
    r=get_recommendation(user["id"],history_id)
    if not r: raise HTTPException(404,"Recommendation not found")
    return {"id":r["id"],"planner_type":r["planner_type"],"created_at":r["created_at"],
            "request":json.loads(r["request_json"]),"response":json.loads(r["response_json"])}

if __name__=="__main__":
    import uvicorn; uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)

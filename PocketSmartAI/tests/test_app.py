import os
from pathlib import Path
os.environ["DATABASE_PATH"]=str(Path(__file__).parent/"test.db")
os.environ["SECRET_KEY"]="test-secret"
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
init_db()
client=TestClient(app)

def test_health():
    r=client.get("/health"); assert r.status_code==200; assert r.json()["status"]=="ok"

def test_register_and_home():
    email="test@example.com"
    client.post("/register",data={"email":email,"password":"password123"})
    r=client.post("/login",data={"email":email,"password":"password123"},follow_redirects=False)
    assert r.status_code==303
    client.cookies.set("access_token",r.cookies.get("access_token"))
    r=client.post("/generate-home",data={"budget":"30000","rooms":"Living Room,Bedroom","style":"modern","city":"India","items":"lighting | 2 | warm"})
    assert r.status_code==200 and r.json()["planner_type"]=="home" and r.json()["history_id"]

def test_party():
    email="party@example.com"
    client.post("/register",data={"email":email,"password":"password123"})
    r=client.post("/login",data={"email":email,"password":"password123"},follow_redirects=False)
    client.cookies.set("access_token",r.cookies.get("access_token"))
    r=client.post("/generate-party",data={"budget":"50000","guests":"50","event_type":"Birthday","venue":"Hall","city":"India","preferences":"vegetarian"})
    assert r.status_code==200 and r.json()["planner_type"]=="party"

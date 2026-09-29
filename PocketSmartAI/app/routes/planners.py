import json
from fastapi import APIRouter, Depends, Form, File, UploadFile, Request, HTTPException
from app.auth import get_current_user
from app.config import settings
from app.database import save_recommendation
from app.models import HomeRequest, PartyRequest, JewelryRequest
from app.services.gemini_service import gemini_service
from app.services.recommendation_service import home_fallback,party_fallback,jewelry_fallback,normalize,add_links

router=APIRouter()

def run_planner(kind,payload,user_id,image=None,mime=None):
    ai=False
    try:
        if not gemini_service.enabled: raise RuntimeError("AI disabled")
        result=normalize(gemini_service.generate(kind,payload,image,mime),float(payload["budget"])); ai=True
    except Exception:
        result={"home":home_fallback,"party":party_fallback,"jewelry":jewelry_fallback}[kind](payload)
    result=add_links(result)
    out={"planner_type":kind,"budget":float(payload["budget"]),"summary":result["summary"],
         "allocation":result["allocation"],"recommendations":result["recommendations"],"ai_generated":ai}
    out["history_id"]=save_recommendation(user_id,kind,json.dumps(payload),json.dumps(out))
    return out

@router.post("/generate-home")
async def home(request:Request,user=Depends(get_current_user)):
    if "application/json" in request.headers.get("content-type",""):
        body=HomeRequest.model_validate(await request.json())
    else:
        f=await request.form()
        items=[]
        for raw in str(f.get("items","")).splitlines():
            if raw.strip():
                p=[x.strip() for x in raw.split("|")]
                items.append({"category":p[0],"quantity":int(p[1]) if len(p)>1 and p[1].isdigit() else 1,"notes":p[2] if len(p)>2 else ""})
        body=HomeRequest(budget=float(f.get("budget",0)),rooms=[x.strip() for x in str(f.get("rooms","Living Room")).split(",") if x.strip()],
                         style=str(f.get("style","modern")),items=items,city=str(f.get("city","India")))
    return run_planner("home",body.model_dump(),user["id"])

@router.post("/generate-party")
async def party(request:Request,user=Depends(get_current_user)):
    if "application/json" in request.headers.get("content-type",""):
        body=PartyRequest.model_validate(await request.json())
    else:
        f=await request.form()
        body=PartyRequest(budget=float(f.get("budget",0)),guests=int(f.get("guests",0)),
                          event_type=str(f.get("event_type","Birthday")),venue=str(f.get("venue","")),
                          city=str(f.get("city","India")),preferences=str(f.get("preferences","")))
    return run_planner("party",body.model_dump(),user["id"])

@router.post("/generate-jewelry")
async def jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("elegant"),
                  outfit_description:str=Form(""),city:str=Form("India"),
                  outfit_image:UploadFile|None=File(None),user=Depends(get_current_user)):
    body=JewelryRequest(budget=budget,occasion=occasion,style=style,outfit_description=outfit_description,city=city).model_dump()
    image=mime=None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}:
            raise HTTPException(400,"Outfit image must be JPG, PNG, or WebP")
        image=await outfit_image.read(); mime=outfit_image.content_type
        if len(image)>settings.max_image_mb*1024*1024: raise HTTPException(413,"Outfit image is too large")
    return run_planner("jewelry",body,user["id"],image,mime)

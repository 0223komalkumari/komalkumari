from app.services.provider_links import provider_search_url

def clamp(items, budget):
    total = sum(float(x["estimated_price"]) for x in items)
    if total <= budget:
        return items
    factor = budget / total * 0.92
    for x in items:
        x["estimated_price"] = round(max(100, x["estimated_price"] * factor), 2)
    return items

def home_fallback(p):
    budget = float(p["budget"])
    base = [
        ("LED ceiling light","lighting",900,"Amazon"),
        ("Decorative floor lamp","lighting",1800,"IKEA"),
        ("Cushion cover set","decor",700,"IKEA"),
        ("Wall art set","decor",1400,"Amazon"),
        ("Compact storage unit","storage",4500,"IKEA"),
        ("Accent chair","seating",6500,"Amazon"),
        ("Side table","furniture",2800,"Flipkart"),
        ("Indoor planter set","decor",1200,"IKEA"),
    ]
    requested = {x["category"].lower() for x in p.get("items", [])}
    rows = []
    for n,c,price,platform in base:
        if not requested or c in requested or c in {"decor","furniture"}:
            rows.append({"name":n,"category":c,"estimated_price":price,"platform":platform,
                         "reason":f"Practical {p.get('style','modern')} option for {', '.join(p['rooms'])}."})
    rows = clamp(rows[:8], budget)
    return {"summary":f"A practical {p.get('style','modern')} setup for {', '.join(p['rooms'])}.",
            "allocation":{"furniture":round(budget*.35,2),"lighting":round(budget*.15,2),
                          "decor":round(budget*.25,2),"storage":round(budget*.25,2)},
            "recommendations":rows}

def party_fallback(p):
    b, g = float(p["budget"]), int(p["guests"])
    rows = [
      {"name":f"Catering package for {g} guests","category":"catering","estimated_price":round(b*.45,2),"platform":"Zomato","reason":f"About ₹{b/g:,.0f} per guest."},
      {"name":"Party decoration package","category":"decoration","estimated_price":round(b*.15,2),"platform":"Amazon","reason":"Flexible base decoration allowance."},
      {"name":"Cake and dessert order","category":"catering","estimated_price":round(b*.10,2),"platform":"Swiggy","reason":"Separate dessert allowance."},
      {"name":"Music / entertainment allowance","category":"entertainment","estimated_price":round(b*.15,2),"platform":"Amazon","reason":"Flexible entertainment allowance."},
      {"name":"Venue allowance","category":"venue","estimated_price":round(b*.10,2),"platform":"OYO","reason":"Search allowance for venue/stay needs."},
      {"name":"Contingency reserve","category":"reserve","estimated_price":round(b*.05,2),"platform":"Amazon","reason":"Buffer for last-minute costs."}
    ]
    return {"summary":f"{p['event_type'].title()} plan for {g} guests in {p.get('city','India')}.",
            "allocation":{"catering":round(b*.55,2),"decoration":round(b*.15,2),
                          "entertainment":round(b*.15,2),"venue":round(b*.10,2),"reserve":round(b*.05,2)},
            "recommendations":rows}

def jewelry_fallback(p):
    b=float(p["budget"])
    rows=[
      {"name":"Statement earrings","category":"earrings","estimated_price":round(b*.25,2),"platform":"Amazon","reason":f"Versatile {p.get('style','elegant')} option for {p['occasion']}."},
      {"name":"Minimal necklace","category":"necklace","estimated_price":round(b*.25,2),"platform":"Flipkart","reason":"Keeps the neckline balanced."},
      {"name":"Bangle / bracelet set","category":"bracelet","estimated_price":round(b*.18,2),"platform":"Amazon","reason":"Adds a coordinated accent."},
      {"name":"Adjustable ring","category":"ring","estimated_price":round(b*.12,2),"platform":"Flipkart","reason":"Lower-cost finishing piece."},
      {"name":"Coordinated jewelry set","category":"set","estimated_price":round(b*.20,2),"platform":"Amazon","reason":"Alternative if a matched set is preferred."}
    ]
    return {"summary":f"Jewelry options for a {p['occasion']} occasion with a {p.get('style','elegant')} direction.",
            "allocation":{"jewelry":round(b*.9,2),"reserve":round(b*.1,2)},"recommendations":rows}

def normalize(data,budget):
    out=[]
    for r in data.get("recommendations",[]):
        try: price=float(r.get("estimated_price",0))
        except (TypeError,ValueError): continue
        if price<=0: continue
        out.append({"name":str(r.get("name","Suggested option"))[:120],
                    "category":str(r.get("category","general"))[:60],
                    "estimated_price":round(price,2),
                    "platform":str(r.get("platform","Amazon"))[:40],
                    "reason":str(r.get("reason","Budget-aware recommendation."))[:300]})
    if not out: raise ValueError("No usable AI recommendations")
    return {"summary":str(data.get("summary","Budget-aware recommendations generated."))[:1000],
            "allocation":data.get("allocation") or {"planned_spend":sum(x["estimated_price"] for x in out)},
            "recommendations":clamp(out[:12],budget)}

def add_links(result):
    for r in result["recommendations"]:
        r["search_url"]=provider_search_url(r["platform"],r["name"])
    return result

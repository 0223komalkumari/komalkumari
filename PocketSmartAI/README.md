# PocketSmart AI

Complete FastAPI + Jinja2 implementation of the supplied PocketSmart AI project.

Features:
- Home Interior Planner
- Party Budget Planner
- Jewelry Planner with optional outfit-image analysis
- Registration, login, logout
- JWT token endpoint
- Session metadata/data endpoints
- Recommendation history
- Gemini integration with deterministic fallback
- Provider search links for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO

The supplied document alternates between Flask and FastAPI; its later milestones explicitly require FastAPI, so this implementation uses FastAPI consistently. Provider links are search links rather than fabricated live catalog APIs.

## Run in VS Code

```text
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000.

For live Gemini, put an API key in `.env` as `GEMINI_API_KEY=...`. Without a key the app still works using fallback recommendations.

Run tests:

```bash
pytest -q
```

## Main endpoints

GET `/health`
POST `/register`
POST `/login`
POST `/token`
GET `/logout`
GET `/session-info`
GET `/session-data`
GET `/history`
POST `/generate-home`
POST `/generate-party`
POST `/generate-jewelry`
GET `/recommendations-details/{history_id}`

## Structure

```text
app/
  main.py config.py database.py auth.py models.py prompts.py
  routes/auth.py routes/pages.py routes/planners.py
  services/gemini_service.py services/provider_links.py services/recommendation_service.py
  templates/
  static/css/styles.css
  static/js/app.js
tests/test_app.py
```

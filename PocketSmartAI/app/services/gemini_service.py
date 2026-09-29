import json
from app.config import settings
from app.prompts import SYSTEM_PROMPT, HOME_PROMPT, PARTY_PROMPT, JEWELRY_PROMPT

class GeminiService:
    def __init__(self):
        self.client = None
        if settings.gemini_api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=settings.gemini_api_key)
            except ImportError:
                self.client = None

    @property
    def enabled(self):
        return self.client is not None

    def _json(self, text):
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        a, b = text.find("{"), text.rfind("}")
        if a < 0 or b < a:
            raise ValueError("Gemini did not return JSON")
        return json.loads(text[a:b+1])

    def generate(self, planner_type, payload, image_bytes=None, image_mime=None):
        if not self.client:
            raise RuntimeError("Gemini not configured")
        from google.genai import types
        prompts = {"home": HOME_PROMPT, "party": PARTY_PROMPT, "jewelry": JEWELRY_PROMPT}
        contents = [SYSTEM_PROMPT + "\n" + prompts[planner_type].format(
            payload=json.dumps(payload, ensure_ascii=False))]
        if image_bytes:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime))
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.35,
                response_mime_type="application/json"
            )
        )
        if not response.text:
            raise ValueError("Empty Gemini response")
        return self._json(response.text)

gemini_service = GeminiService()

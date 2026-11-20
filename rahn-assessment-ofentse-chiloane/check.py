from dotenv import load_dotenv
load_dotenv()
import os
from google import genai

print("key set:", bool(os.getenv("GEMINI_API_KEY")))
print("model:", os.getenv("GEMINI_MODEL"))
try:
    c = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    r = c.models.generate_content(model=os.getenv("GEMINI_MODEL"), contents="say hi")
    print("OK:", r.text)
except Exception as e:
    print("ERROR:", type(e).__name__, repr(e)[:300])



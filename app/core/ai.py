import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.6-flash")

def ask_gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
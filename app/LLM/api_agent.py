from fastapi import FastAPI
from pydantic import BaseModel
import requests
import google.generativeai as genai
import openai

# Initialize FastAPI
app = FastAPI(title="Gemini + ChatGPT Weather Advisor")

# API Keys
OPENAI_API_KEY = "your_openai_api_key"
WEATHER_API_KEY = "your_openweather_api_key"
GEMINI_API_KEY = "your_gemini_api_key"

# Configure APIs
openai.api_key = OPENAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Request model
class WeatherRequest(BaseModel):
    city: str

@app.post("/weather-advice")
def weather_advice(request: WeatherRequest):
    city = request.city

    # Step 1: Gemini fetches weather data
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    gemini_prompt = f"Make an HTTP GET request to {weather_url} and return the JSON response."
    gemini_response = genai.GenerativeModel("gemini-2.5-flash").generate_content(gemini_prompt)
    
    # Extract JSON from Gemini response
    weather_data = gemini_response.text  # Assuming Gemini returns raw JSON
    # (Optional: parse JSON if needed)

    # Step 2: ChatGPT analyzes and suggests clothing
    print(weather_data)
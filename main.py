from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY")


# 🔹 Simulated "model" (AI logic)
def weather_advisor(temp, description):
    advice = ""
    warning = ""

    # Basic advice
    if temp < 10:
        advice = "Wear a heavy jacket 🧥"
    elif 10 <= temp < 20:
        advice = "Light jacket recommended 🧢"
    elif 20 <= temp < 30:
        advice = "Comfortable weather 😎"
    else:
        advice = "Stay hydrated! Very hot 🔥"

    # ⚠️ Precaution logic (NEW FEATURE)
    if "rain" in description.lower():
        warning = "⚠️ Carry an umbrella ☔"
    elif "snow" in description.lower():
        warning = "⚠️ Roads may be slippery ❄️"
    elif temp > 35:
        warning = "⚠️ Heat risk! Avoid outdoor activities"
    elif temp < 0:
        warning = "⚠️ Freezing temperature! Stay warm"

    return advice, warning


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Weather AI App 🌤️</h2>
    <form action="/weather">
        <input name="city" placeholder="Enter city"/>
        <button type="submit">Search</button>
    </form>
    """


@app.get("/weather", response_class=HTMLResponse)
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if "main" not in response:
        return "<h3>City not found ❌</h3><a href='/'>Back</a>"

    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]

    # 🔥 AI model output
    advice, warning = weather_advisor(temp, desc)

    return f"""
    <html>
        <body style="font-family:Arial; text-align:center;">
            <h2>Weather in {city}</h2>
            <p>🌡 Temperature: {temp}°C</p>
            <p>☁️ Condition: {desc}</p>
            <h3>🤖 AI Advice: {advice}</h3>
            <h3 style="color:red;">{warning}</h3>
            <br>
            <a href="/">Back</a>
        </body>
    </html>
    """
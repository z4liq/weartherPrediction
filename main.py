from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

API_KEY = "7c49591665c3b7d90de8b57391b3260b"

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h2>Weather App</h2>
            <form action="/weather">
                <input name="city" placeholder="Enter city"/>
                <button type="submit">Search</button>
            </form>
        </body>
    </html>
    """

@app.get("/weather", response_class=HTMLResponse)
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]

    return f"""
    <html>
        <body>
            <h2>Weather in {city}</h2>
            <p>🌡 Temperature: {temp}°C</p>
            <p>☁️ Condition: {desc}</p>
            <a href="/">Back</a>
        </body>
    </html>
    """
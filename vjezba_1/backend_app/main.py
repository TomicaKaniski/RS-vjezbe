import os

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Vremenska prognoza API", version="1.0.0")
render_origin = "https://rs-vjezbe-vjezba-1-frontend-app-tk.onrender.com"

allowed_origins = ["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8080", "http://127.0.0.1:8080", render_origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Vremenska prognoza API", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "weather-api"}


@app.get("/api/cities")
def cities():
    return {"cities": ["Zagreb", "Pula", "Rijeka", "Split", "Osijek"]}


@app.get("/api/weather")
async def weather(city: str = Query(default="Zagreb", min_length=2, max_length=80)):
    """Pronađi grad i vrati trenutno vrijeme s javnog Open-Meteo servisa."""
    city = city.strip()
    if len(city) < 2:
        raise HTTPException(status_code=422, detail="Unesi naziv grada s barem 2 znaka.")

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            geo = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "hr"},
            )
            geo.raise_for_status()
            locations = geo.json().get("results", [])
            if not locations:
                raise HTTPException(status_code=404, detail="Grad nije pronađen.")

            place = locations[0]
            forecast = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,is_day",
                    "timezone": "auto",
                },
            )
            forecast.raise_for_status()
            current = forecast.json()["current"]

    except (httpx.RequestError, httpx.HTTPStatusError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="Servis za vremensku prognozu trenutno nije dostupan.") from exc

    return {
        "city": place["name"],
        "country": place.get("country_code", ""),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
        "is_day": bool(current["is_day"]),
        "updated_at": current["time"],
    }

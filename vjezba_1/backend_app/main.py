import os

import logging

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Vremenska prognoza API", version="1.0.0")
render_origin = "https://rs-vjezbe-vjezba-1-frontend-app-tk.onrender.com"

allowed_origins = ["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8080", "http://127.0.0.1:8080", render_origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

DUMMY_WEATHER = {
    "Zagreb": {"temperature": 18, "feels_like": 17, "humidity": 62, "wind": 12, "weather_code": 2},
    "Pula":   {"temperature": 23, "feels_like": 24, "humidity": 55, "wind": 8,  "weather_code": 0},
    "Rijeka": {"temperature": 20, "feels_like": 19, "humidity": 78, "wind": 18, "weather_code": 3},
    "Split":  {"temperature": 25, "feels_like": 26, "humidity": 48, "wind": 10, "weather_code": 1},
    "Osijek": {"temperature": 16, "feels_like": 14, "humidity": 70, "wind": 15, "weather_code": 61},
}

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

        logger.warning("Open-Meteo unavailable: %s", exc)

        if city not in DUMMY_WEATHER:
            raise HTTPException(status_code=503, detail="Nema podataka za ovaj grad.")

        return {
            "source": "demo",
            "city": city,
            "country": "HR",
            **DUMMY_WEATHER[city],
            "is_day": True,
            "updated_at": datetime.now().isoformat(timespec="minutes")
        }

    return {
        "source": "open-meteo",
        "city": place["name"],
        "country": place.get("country_code", ""),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
        "is_day": bool(current["is_day"]),
        "updated_at": current["time"]
    }

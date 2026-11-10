"""REST API: Gregorian to Hebrew date conversion."""
import datetime

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from logic.converter import convert_to_hebrew

app = FastAPI()


class ConvertRequest(BaseModel):
    date: datetime.date


@app.post("/api/convert")
def convert(request: ConvertRequest) -> dict:
    """Convert the given Gregorian date to a Hebrew date."""
    try:
        return convert_to_hebrew(
            request.date.year, request.date.month, request.date.day
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Hebcal unavailable")


# Mounted last so that /api/convert takes precedence.
app.mount("/", StaticFiles(directory="front", html=True), name="front")

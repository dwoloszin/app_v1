from pydantic import BaseModel
from datetime import datetime
from typing import List

class WeatherData(BaseModel):
    city_id: int
    temperature: float
    humidity: int
    request_datetime: datetime

class WeatherRequest(BaseModel):
    user_id: str
    city_ids: List[int]

class ProgressResponse(BaseModel):
    user_id: str
    progress_percentage: float

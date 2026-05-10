from pydantic import BaseModel
from datetime import datetime
from typing import List

class WeatherReading(BaseModel):
    temperature: float
    windspeed: float
    winddirection: int
    time: datetime
    weathercode: int
    is_day: int
    interval: int

class HourlyWeather(BaseModel):
    time: List[datetime]
    temperature_2m: List[float]
    windspeed_10m: List[float]
    weathercode: List[int]
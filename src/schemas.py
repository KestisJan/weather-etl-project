from pydantic import BaseModel
from datetime import datetime

class WeatherReading(BaseModel):
    temperature: float
    windspeed: float
    winddirection: int
    time: datetime
    weathercode: int
    is_day: int
    interval: int
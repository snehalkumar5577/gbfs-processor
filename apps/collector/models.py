from pydantic import BaseModel
from datetime import datetime

class StationData(BaseModel):
    provider: str
    station_id: str
    timestamp: datetime
    available_bikes: int
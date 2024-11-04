from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict

class StationData(BaseModel):
    provider: str
    data: Dict[str, Any]
    timestamp: datetime
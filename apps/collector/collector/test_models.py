import pytest
from datetime import datetime
from pydantic import ValidationError
from collector.models import StationData

def test_station_data_creation():
    data = {
        "provider": "TestProvider",
        "station_id": "123",
        "timestamp": datetime.now(),
        "available_bikes": 10
    }
    station_data = StationData(**data)
    assert station_data.provider == "TestProvider"
    assert station_data.station_id == "123"
    assert station_data.available_bikes == 10

def test_station_data_missing_fields():
    data = {
        "provider": "TestProvider",
        "station_id": "123",
        "timestamp": datetime.now()
    }
    with pytest.raises(ValidationError):
        StationData(**data)

def test_station_data_invalid_types():
    data = {
        "provider": "TestProvider",
        "station_id": "123",
        "timestamp": "not-a-datetime",
        "available_bikes": "not-an-int"
    }
    with pytest.raises(ValidationError):
        StationData(**data)
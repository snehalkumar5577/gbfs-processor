import pytest
from unittest.mock import patch, MagicMock
from collector.fetcher import fetch_data, get_station_info_url, extract_station_info
from requests.exceptions import RequestException

def test_fetch_data_success():
    url = "http://example.com"
    mock_response = MagicMock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status = MagicMock()

    with patch('collector.fetcher.requests.get', return_value=mock_response):
        data = fetch_data(url)
        assert data == {"key": "value"}

def test_fetch_data_failure():
    url = "http://example.com"
    with patch('collector.fetcher.requests.get', side_effect=RequestException("Error")):
        data = fetch_data(url)
        assert data is None

def test_get_station_info_url():
    feeds = [
        {"name": "station_status", "url": "http://example.com/station_info"},
        {"name": "free_bike_status", "url": "http://example.com/free_bike_status"}
    ]
    url = get_station_info_url(feeds)
    assert url == "http://example.com/station_info"

def test_get_station_info_url_not_found():
    feeds = [
        {"name": "free_bike_status", "url": "http://example.com/free_bike_status"}
    ]
    url = get_station_info_url(feeds)
    assert url is None

def test_extract_station_info_success():
    provider_name = "test_provider"
    provider_url = "http://example.com"
    mock_gbfs_data = {
        "data": {
            "en": {
                "feeds": [
                    {"name": "station_status", "url": "http://example.com/station_info"}
                ]
            }
        }
    }
    mock_station_info = {"data": {"stations": [{"station_id": "123", "name": "Station 123"}]}}

    with patch('collector.fetcher.fetch_data', side_effect=[mock_gbfs_data, mock_station_info]):
        station_info = extract_station_info(provider_name, provider_url)
        assert station_info == mock_station_info

def test_extract_station_info_failure():
    provider_name = "test_provider"
    provider_url = "http://example.com"

    with patch('collector.fetcher.fetch_data', return_value=None):
        station_info = extract_station_info(provider_name, provider_url)
        assert station_info is None
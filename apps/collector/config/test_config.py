import json
from config.config import get_config, Config, DevelopmentConfig, ProductionConfig


def test_get_config_development(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "dev")
    config_class = get_config()
    assert config_class == DevelopmentConfig

def test_get_config_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "prod")
    config_class = get_config()
    assert config_class == ProductionConfig

def test_config_default_providers():
    config = Config()
    assert config.PROVIDERS == {
        "Careem BIKE": "https://dubai.publicbikesystem.net/customer/gbfs/v2/gbfs.json",
        "Blue-bike": "https://api.delijn.be/gbfs/gbfs.json",
        "Zenica": "https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bz/gbfs.json"
    }

# def test_config_override_providers(monkeypatch):
#     custom_providers = {
#         "Test Provider": "https://test.provider/gbfs.json"
#     }
#     monkeypatch.setenv("PROVIDERS_JSON", json.dumps(custom_providers))
#     config = Config()
#     assert config.PROVIDERS == custom_providers
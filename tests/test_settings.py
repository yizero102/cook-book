import pytest
from config.settings import Settings


class TestSettings:
    def test_settings_initialization(self, settings):
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_settings_has_required_fields(self, settings):
        assert hasattr(settings, 'anthropic_api_key')
        assert hasattr(settings, 'anthropic_base_url')
        assert hasattr(settings, 'model_name')
        assert hasattr(settings, 'max_tokens')
        assert hasattr(settings, 'temperature')
    
    def test_settings_validation_success(self, settings):
        is_valid, error_msg = settings.validate()
        assert is_valid is True
        assert error_msg is None
    
    def test_settings_default_values(self):
        settings = Settings(
            anthropic_api_key="test_key",
            anthropic_base_url="https://test.com",
            model_name="test_model"
        )
        assert settings.max_tokens == 4096
        assert settings.temperature == 0.7
    
    def test_settings_custom_values(self):
        settings = Settings(
            anthropic_api_key="test_key",
            anthropic_base_url="https://test.com",
            model_name="test_model",
            max_tokens=2048,
            temperature=0.5
        )
        assert settings.max_tokens == 2048
        assert settings.temperature == 0.5

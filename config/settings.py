import os
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Settings(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    
    anthropic_api_key: str = Field(default_factory=lambda: os.getenv("_ANTHROPIC_API_KEY", ""))
    anthropic_base_url: str = Field(default_factory=lambda: os.getenv("_ANTHROPIC_BASE_URL", "https://api.anthropic.com"))
    model_name: str = Field(default_factory=lambda: os.getenv("_MODEL_NAME", "claude-3-5-sonnet-20241022"))
    max_tokens: int = Field(default=4096)
    temperature: float = Field(default=0.7)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        if not self.anthropic_api_key:
            return False, "ANTHROPIC_API_KEY is not set"
        if not self.anthropic_base_url:
            return False, "ANTHROPIC_BASE_URL is not set"
        if not self.model_name:
            return False, "MODEL_NAME is not set"
        return True, None

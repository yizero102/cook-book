import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.settings import Settings
from src.ai_mirror import AIMirrorClient
from src.ai_mirror.tools import create_example_tools


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def client(settings):
    return AIMirrorClient(settings)


@pytest.fixture
def client_with_tools(settings):
    tool_registry = create_example_tools()
    return AIMirrorClient(settings, tool_registry)


@pytest.fixture
def tool_registry():
    return create_example_tools()

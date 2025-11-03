import pytest
from src.ai_mirror import AIMirrorClient
from config.settings import Settings
from src.ai_mirror.tools import create_example_tools


class TestAIMirrorClient:
    def test_client_initialization(self, client):
        assert client is not None
        assert isinstance(client, AIMirrorClient)
        assert client.client is not None
    
    def test_client_with_settings(self, settings):
        client = AIMirrorClient(settings)
        assert client.settings == settings
    
    def test_client_verify_connection(self, client):
        success, message = client.verify_connection()
        assert success is True
        assert "successful" in message.lower()
    
    def test_client_basic_chat(self, client):
        response = client.chat("What is 2+2?")
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_client_chat_with_system_prompt(self, client):
        response = client.chat(
            "Say hello",
            system_prompt="You are a friendly assistant who always greets warmly."
        )
        assert response is not None
        assert len(response) > 0
    
    def test_client_set_system_prompt(self, client):
        client.set_system_prompt("You are a helpful assistant.")
        system_msg = client.conversation.get_system_message()
        assert system_msg is not None
        assert "helpful" in system_msg.lower()
    
    def test_client_clear_conversation(self, client):
        client.chat("Hello")
        assert len(client.conversation.messages) > 0
        
        client.clear_conversation()
        assert len(client.conversation.messages) == 0
    
    def test_client_get_conversation_history(self, client):
        client.chat("Hello")
        history = client.get_conversation_history()
        
        assert "messages" in history
        assert len(history["messages"]) > 0
    
    def test_client_multiple_messages(self, client):
        client.chat("Hello")
        client.chat("How are you?")
        
        history = client.get_conversation_history()
        assert len(history["messages"]) >= 4
    
    def test_client_get_settings(self, client, settings):
        client_settings = client.get_settings()
        assert client_settings.model_name == settings.model_name
        assert client_settings.anthropic_base_url == settings.anthropic_base_url


class TestAIMirrorClientWithTools:
    def test_client_with_tools_initialization(self, client_with_tools):
        assert client_with_tools is not None
        assert client_with_tools.tool_registry.has_tools() is True
    
    def test_client_tools_available(self, client_with_tools):
        tools = client_with_tools.tool_registry.get_all_tools()
        assert len(tools) > 0
        
        calculator = client_with_tools.tool_registry.get("calculator")
        assert calculator is not None


class TestAIMirrorClientErrorHandling:
    def test_client_invalid_settings(self):
        with pytest.raises(ValueError):
            invalid_settings = Settings(
                anthropic_api_key="",
                anthropic_base_url="",
                model_name=""
            )
            AIMirrorClient(invalid_settings)
    
    def test_client_handles_empty_message(self, client):
        response = client.chat("")
        assert response is not None


class TestAIMirrorClientIntegration:
    def test_full_conversation_flow(self, client):
        client.set_system_prompt("You are a math tutor.")
        
        response1 = client.chat("What is 5 + 3?")
        assert response1 is not None
        
        response2 = client.chat("And what is that multiplied by 2?")
        assert response2 is not None
        
        history = client.get_conversation_history()
        assert len(history["messages"]) >= 5
    
    def test_conversation_context_maintained(self, client):
        client.chat("My name is Alice.")
        response = client.chat("What is my name?")
        
        assert response is not None
    
    def test_clear_and_restart_conversation(self, client):
        client.chat("Hello")
        client.clear_conversation()
        
        response = client.chat("What did I just say?")
        assert response is not None

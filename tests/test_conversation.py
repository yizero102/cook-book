import pytest
from src.ai_mirror.conversation import Conversation, Message


class TestMessage:
    def test_message_creation(self):
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.timestamp is not None
    
    def test_message_to_dict(self):
        msg = Message(role="assistant", content="Hi there")
        msg_dict = msg.to_dict()
        assert msg_dict["role"] == "assistant"
        assert msg_dict["content"] == "Hi there"
    
    def test_message_with_metadata(self):
        metadata = {"source": "test", "priority": "high"}
        msg = Message(role="user", content="Test", metadata=metadata)
        assert msg.metadata == metadata


class TestConversation:
    def test_conversation_initialization(self):
        conv = Conversation()
        assert conv.messages == []
        assert conv.conversation_id is None
    
    def test_add_message(self):
        conv = Conversation()
        conv.add_message("user", "Hello")
        assert len(conv.messages) == 1
        assert conv.messages[0].role == "user"
        assert conv.messages[0].content == "Hello"
    
    def test_add_multiple_messages(self):
        conv = Conversation()
        conv.add_message("user", "Hello")
        conv.add_message("assistant", "Hi there")
        conv.add_message("user", "How are you?")
        assert len(conv.messages) == 3
    
    def test_get_messages_for_api(self):
        conv = Conversation()
        conv.add_message("system", "You are helpful")
        conv.add_message("user", "Hello")
        conv.add_message("assistant", "Hi")
        
        api_messages = conv.get_messages_for_api()
        assert len(api_messages) == 2
        assert all(msg["role"] != "system" for msg in api_messages)
    
    def test_get_system_message(self):
        conv = Conversation()
        conv.add_message("system", "Be helpful")
        conv.add_message("system", "Be concise")
        conv.add_message("user", "Hello")
        
        system_msg = conv.get_system_message()
        assert "Be helpful" in system_msg
        assert "Be concise" in system_msg
    
    def test_clear_conversation(self):
        conv = Conversation()
        conv.add_message("user", "Hello")
        conv.add_message("assistant", "Hi")
        conv.clear()
        assert len(conv.messages) == 0
    
    def test_get_last_message(self):
        conv = Conversation()
        conv.add_message("user", "First")
        conv.add_message("assistant", "Second")
        
        last_msg = conv.get_last_message()
        assert last_msg is not None
        assert last_msg.content == "Second"
    
    def test_get_last_message_empty(self):
        conv = Conversation()
        last_msg = conv.get_last_message()
        assert last_msg is None
    
    def test_to_dict(self):
        conv = Conversation()
        conv.conversation_id = "test_123"
        conv.add_message("user", "Hello")
        
        conv_dict = conv.to_dict()
        assert conv_dict["conversation_id"] == "test_123"
        assert len(conv_dict["messages"]) == 1

import pytest
from src.ai_mirror.tools import Tool, ToolRegistry, create_example_tools


class TestTool:
    def test_tool_creation(self):
        tool = Tool(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object", "properties": {}}
        )
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
    
    def test_tool_to_anthropic_format(self):
        tool = Tool(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object"}
        )
        anthropic_format = tool.to_anthropic_format()
        assert anthropic_format["name"] == "test_tool"
        assert anthropic_format["description"] == "A test tool"
        assert "input_schema" in anthropic_format


class TestToolRegistry:
    def test_registry_initialization(self):
        registry = ToolRegistry()
        assert len(registry.tools) == 0
    
    def test_register_tool(self):
        registry = ToolRegistry()
        tool = Tool(
            name="test_tool",
            description="Test",
            input_schema={}
        )
        registry.register(tool)
        assert len(registry.tools) == 1
        assert registry.get("test_tool") == tool
    
    def test_get_nonexistent_tool(self):
        registry = ToolRegistry()
        assert registry.get("nonexistent") is None
    
    def test_get_all_tools(self):
        registry = ToolRegistry()
        tool1 = Tool(name="tool1", description="Test1", input_schema={})
        tool2 = Tool(name="tool2", description="Test2", input_schema={})
        registry.register(tool1)
        registry.register(tool2)
        
        all_tools = registry.get_all_tools()
        assert len(all_tools) == 2
    
    def test_has_tools(self):
        registry = ToolRegistry()
        assert registry.has_tools() is False
        
        tool = Tool(name="tool", description="Test", input_schema={})
        registry.register(tool)
        assert registry.has_tools() is True
    
    def test_to_anthropic_format(self):
        registry = ToolRegistry()
        tool = Tool(name="tool", description="Test", input_schema={})
        registry.register(tool)
        
        anthropic_format = registry.to_anthropic_format()
        assert len(anthropic_format) == 1
        assert anthropic_format[0]["name"] == "tool"


class TestExampleTools:
    def test_create_example_tools(self):
        registry = create_example_tools()
        assert registry.has_tools() is True
        
        calculator = registry.get("calculator")
        assert calculator is not None
        assert calculator.name == "calculator"
    
    @pytest.mark.asyncio
    async def test_calculator_tool_add(self):
        registry = create_example_tools()
        calculator = registry.get("calculator")
        
        result = await calculator.handler(operation="add", a=5, b=3)
        assert "8" in result
    
    @pytest.mark.asyncio
    async def test_calculator_tool_multiply(self):
        registry = create_example_tools()
        calculator = registry.get("calculator")
        
        result = await calculator.handler(operation="multiply", a=6, b=7)
        assert "42" in result
    
    @pytest.mark.asyncio
    async def test_calculator_tool_divide_by_zero(self):
        registry = create_example_tools()
        calculator = registry.get("calculator")
        
        result = await calculator.handler(operation="divide", a=10, b=0)
        assert "Error" in result or "zero" in result.lower()

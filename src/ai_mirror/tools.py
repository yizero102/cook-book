from typing import Callable, Dict, Any, List, Optional
from pydantic import BaseModel, Field
import json


class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Optional[Callable] = Field(default=None, exclude=True)
    
    def to_anthropic_format(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }
    
    async def execute(self, **kwargs) -> Any:
        if self.handler:
            return await self.handler(**kwargs) if callable(self.handler) else None
        return None


class ToolRegistry(BaseModel):
    tools: Dict[str, Tool] = Field(default_factory=dict)
    
    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)
    
    def get_all_tools(self) -> List[Tool]:
        return list(self.tools.values())
    
    def to_anthropic_format(self) -> List[Dict[str, Any]]:
        return [tool.to_anthropic_format() for tool in self.tools.values()]
    
    def has_tools(self) -> bool:
        return len(self.tools) > 0


def create_example_tools() -> ToolRegistry:
    registry = ToolRegistry()
    
    calculator_tool = Tool(
        name="calculator",
        description="Perform basic arithmetic operations",
        input_schema={
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    )
    
    async def calculator_handler(operation: str, a: float, b: float) -> str:
        operations = {
            "add": a + b,
            "subtract": a - b,
            "multiply": a * b,
            "divide": a / b if b != 0 else "Error: Division by zero"
        }
        result = operations.get(operation, "Error: Unknown operation")
        return json.dumps({"result": result})
    
    calculator_tool.handler = calculator_handler
    registry.register(calculator_tool)
    
    return registry

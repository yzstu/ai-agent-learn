from .calculator import CalculatorTool
from .web_search import WebSearchTool

class ToolManager:
    """工具管理器"""
    def __init__(self):
        self.tools = {
            "calculator": CalculatorTool(),
            "web_search": WebSearchTool()
        }
    
    def get_tool(self, name: str):
        return self.tools.get(name)
    
    def get_available_tools(self):
        return list(self.tools.keys())
    
    def get_tools_schema(self):
        return [tool.get_schema() for tool in self.tools.values()]
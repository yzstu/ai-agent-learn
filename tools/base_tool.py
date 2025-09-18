from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseTool(ABC):
    """工具基类"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """执行工具并返回结果"""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """返回工具的调用schema，用于Function Calling"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self._get_parameter_schema(),
                "required": self._get_required_parameters()
            }
        }
    
    @abstractmethod
    def _get_parameter_schema(self) -> Dict[str, Any]:
        """返回参数schema"""
        pass
    
    @abstractmethod
    def _get_required_parameters(self) -> List[str]:
        """返回必需参数列表"""
        pass
import math
from typing import Dict, Any, List
from .base_tool import BaseTool

class CalculatorTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="执行数学计算，支持加减乘除、幂运算、平方根等"
        )
    
    def execute(self, expression: str) -> str:
        try:
            # 安全地评估数学表达式
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    def _get_parameter_schema(self) -> Dict[str, Any]:
        return {
            "expression": {
                "type": "string",
                "description": "数学表达式，例如: '2 + 3 * 4', 'sqrt(16)', 'sin(30)'"
            }
        }
    
    def _get_required_parameters(self) -> List[str]:
        return ["expression"]
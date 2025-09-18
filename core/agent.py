import re
import json
from typing import Dict, Any, List
from .models import ModelManager
from .prompts import get_system_prompt, format_tool_descriptions
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from tools import ToolManager

class AIAgent:
    """AI Agent 主类"""
    def __init__(self):
        self.model_manager = ModelManager()
        self.tool_manager = ToolManager()
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory()
        
        # 初始化系统提示词
        tool_descriptions = format_tool_descriptions(
            [self.tool_manager.get_tool(name) for name in self.tool_manager.get_available_tools()]
        )
        self.system_prompt = get_system_prompt(tool_descriptions)
        
        # 添加系统提示词到历史
        self.short_term_memory.add_message("system", self.system_prompt)
    
    def set_model(self, model_name: str):
        """设置使用的模型"""
        self.model_manager.set_model(model_name)
    
    def process_message(self, user_input: str) -> str:
        """处理用户输入并返回响应"""
        # 添加用户消息到历史
        self.short_term_memory.add_message("user", user_input)
        
        # 从长期记忆中检索相关信息
        relevant_memories = self.long_term_memory.retrieve_memories(user_input)
        if relevant_memories:
            memory_context = "\n相关记忆:\n" + "\n".join(relevant_memories)
            enhanced_input = user_input + memory_context
            self.short_term_memory.add_message("user", enhanced_input)
        
        # 获取模型响应
        response = self._get_model_response()
        
        # 处理可能的多轮工具调用
        final_response = self._handle_tool_calls(response)
        
        # 添加助手响应到历史
        self.short_term_memory.add_message("assistant", final_response)
        
        # 存储到长期记忆
        self.long_term_memory.store_memory(
            f"用户: {user_input}\n助手: {final_response}",
            {"type": "conversation"}
        )
        
        return final_response
    
    def _get_model_response(self) -> str:
        """获取模型初始响应"""
        history = self.short_term_memory.get_history()
        return self.model_manager.chat_completion(history)
    
    def _handle_tool_calls(self, initial_response: str) -> str:
        """处理模型响应中的工具调用"""
        response = initial_response
        max_iterations = 5  # 防止无限循环
        
        for _ in range(max_iterations):
            # 检查是否需要工具调用
            if "行动:" in response and "行动输入:" in response:
                # 提取工具名称和输入
                tool_match = re.search(r"行动:\s*([^\n]+)", response)
                input_match = re.search(r"行动输入:\s*(\{.*\})", response, re.DOTALL)
                
                if tool_match and input_match:
                    tool_name = tool_match.group(1).strip()
                    tool_input_json = input_match.group(1).strip()
                    
                    try:
                        # 执行工具
                        tool = self.tool_manager.get_tool(tool_name)
                        if tool:
                            tool_input = json.loads(tool_input_json)
                            tool_result = tool.execute(**tool_input)
                            
                            # 添加工具执行结果到历史
                            self.short_term_memory.add_message("user", f"观察: {tool_result}")
                            
                            # 获取模型的下一个响应
                            history = self.short_term_memory.get_history()
                            response = self.model_manager.chat_completion(history)
                        else:
                            response = f"错误: 未知工具 '{tool_name}'"
                            break
                    except json.JSONDecodeError:
                        response = "错误: 行动输入不是有效的JSON格式"
                        break
                    except Exception as e:
                        response = f"工具执行错误: {str(e)}"
                        break
                else:
                    break
            else:
                break
        
        # 提取最终回答
        if "最终回答:" in response:
            final_match = re.search(r"最终回答:\s*(.+)", response, re.DOTALL)
            if final_match:
                return final_match.group(1).strip()
        
        return response
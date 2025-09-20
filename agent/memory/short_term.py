from typing import List, Dict, Any
from config.settings import settings

class ShortTermMemory:
    """短期记忆 - 管理对话历史"""
    def __init__(self):
        self.history: List[Dict[str, str]] = []
        self.max_length = settings.MAX_HISTORY_LENGTH
    
    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        self.history.append({"role": role, "content": content})
        
        # 限制历史长度
        if len(self.history) > self.max_length:
            self.history = self.history[-self.max_length:]
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.history.copy()
    
    def clear(self):
        """清空对话历史"""
        self.history = []
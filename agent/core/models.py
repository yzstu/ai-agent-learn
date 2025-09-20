import ollama
import requests
import json
from typing import Dict, Any, List
from config.settings import settings

class ModelProvider:
    """模型提供商基类"""
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        raise NotImplementedError

class SiliconFlowModel(ModelProvider):
    """硅基流动模型"""
    def __init__(self):
        self.api_key = settings.SILICONFLOW_API_KEY
        self.model = settings.SILICONFLOW_MODEL
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            **kwargs
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error calling SiliconFlow API: {str(e)}"

class OllamaModel(ModelProvider):
    """Ollama 本地模型"""
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # 将对话历史转换为 Ollama 格式
        # 注意: Ollama 的 API 格式与 OpenAI 略有不同
        prompt = self._format_messages(messages)
        
        try:
            # 异步生成
            response = ollama.Client().generate(
                model=self.model,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            return f"Error calling Ollama API: {str(e)}"
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """将消息列表格式化为 Ollama 所需的提示格式"""
        formatted = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                formatted += f"System: {content}\n\n"
            elif role == "user":
                formatted += f"User: {content}\n\n"
            elif role == "assistant":
                formatted += f"Assistant: {content}\n\n"
        return formatted

class ModelManager:
    """模型管理器，支持切换不同模型"""
    def __init__(self):
        self.models = {
            "siliconflow": SiliconFlowModel(),
            "ollama": OllamaModel()
        }
        self.current_model = "ollama"  # 默认使用 Ollama
    
    def set_model(self, model_name: str):
        if model_name in self.models:
            self.current_model = model_name
        else:
            raise ValueError(f"Unknown model: {model_name}")
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        return self.models[self.current_model].chat_completion(messages, **kwargs)
import os
import requests
import json
from typing import Any, List, Mapping, Optional, Dict, Union, Iterator
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage, ChatResult, ChatGeneration
from langchain.callbacks.manager import CallbackManagerForLLMRun
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SiliconFlowChat(BaseChatModel, BaseModel):
    """硅基流动聊天模型实现"""
    
    api_key: str = Field(default_factory=lambda: os.getenv("SILICONFLOW_API_KEY"))
    api_base: str = Field(default="https://api.siliconflow.cn/v1")
    model: str = Field(default="your-model-name")  # 替换为你的模型名称
    
    # 模型参数
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=1000)
    top_p: float = Field(default=0.9)
    
    @property
    def _llm_type(self) -> str:
        return "siliconflow-chat"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """生成聊天响应"""
        try:
            # 准备请求头
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 格式化消息为硅基流动API所需的格式
            formatted_messages = []
            for message in messages:
                if isinstance(message, HumanMessage):
                    formatted_messages.append({"role": "user", "content": message.content})
                elif isinstance(message, AIMessage):
                    formatted_messages.append({"role": "assistant", "content": message.content})
                elif isinstance(message, SystemMessage):
                    formatted_messages.append({"role": "system", "content": message.content})
            
            # 准备请求体
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p,
                "stop": stop if stop else []
            }
            
            # 发送请求
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                error_msg = f"API请求失败: {response.status_code}, {response.text}"
                raise Exception(error_msg)
                
            # 解析响应
            result = response.json()
            message_content = result["choices"][0]["message"]["content"]
            
            # 创建ChatResult对象
            return ChatResult(
                generations=[ChatGeneration(message=AIMessage(content=message_content))]
            )
            
        except Exception as e:
            raise Exception(f"调用硅基流动API时出错: {str(e)}")
    
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatResult]:
        """流式生成响应"""
        # 这里可以实现流式响应，但需要硅基流动API支持流式传输
        # 目前先调用普通生成方法
        result = self._generate(messages, stop, run_manager, **kwargs)
        yield result
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """返回标识参数"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }

# 使用示例
def main():
    # 初始化硅基流动聊天模型
    chat_model = SiliconFlowChat(
        api_key="sk-zvsrqozpkfkvwxtxxehsztxxiogumdhlgwdgcacuwhaugkcj",
        model="deepseek-ai/DeepSeek-V3",  # 替换为你的模型名称
        temperature=0.7,
        max_tokens=1000
    )
    
    # 创建消息列表
    messages = [
        SystemMessage(content="你是一个有帮助的AI助手。"),
        HumanMessage(content="请解释一下人工智能的基本概念")
    ]
    
    try:
        # 使用正确的方法调用模型
        result = chat_model._generate(messages)
        print("响应:", result.generations[0].message.content)
        
        # 或者使用predict_messages方法（如果可用）
        response = chat_model.predict_messages(messages)
        print("预测响应:", response.content)
        
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
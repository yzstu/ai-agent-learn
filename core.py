# ...existing code...
import requests

class MyAgent:
    # ...existing code...

    @staticmethod
    def call_ollama_model(prompt: str, model_name: str = "default", host: str = "http://localhost:8000"):
        """
        调用本地部署的 Ollama 模型。
        :param prompt: 输入的提示文本
        :param model_name: 模型名称
        :param host: 本地 Ollama 服务的地址
        :return: 模型生成的响应
        """
        url = f"{host}/api/v1/generate"
        payload = {
            "model": model_name,
            "prompt": prompt
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("text", "")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"调用 Ollama 模型失败: {e}")

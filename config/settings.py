import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 模型配置
    SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
    SILICONFLOW_MODEL = os.getenv("SILICONFLOW_MODEL")
    
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    
    # 记忆配置
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
    
    # Agent 配置
    MAX_HISTORY_LENGTH = 10  # 最大对话历史长度

settings = Settings()
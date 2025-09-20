import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from config.settings import settings

class LongTermMemory:
    """长期记忆 - 使用向量数据库存储和检索信息"""
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # 创建或获取集合
        self.collection = self.client.get_or_create_collection("agent_memory")
    
    def store_memory(self, text: str, metadata: Dict[str, Any] = None):
        """存储记忆到向量数据库"""
        if metadata is None:
            metadata = {}
        
        # 生成ID（在实际应用中可能需要更复杂的ID生成策略）
        import uuid
        memory_id = str(uuid.uuid4())
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id]
        )
    
    def retrieve_memories(self, query: str, n_results: int = 3) -> List[str]:
        """从向量数据库中检索相关记忆"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results["documents"][0] if results["documents"] else []
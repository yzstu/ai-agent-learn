import requests
from typing import Dict, Any, List
from .base_tool import BaseTool

class WebSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="在互联网上搜索最新信息"
        )
    
    def execute(self, query: str, max_results: int = 3) -> str:
        # 这里使用DuckDuckGo的API，你也可以替换为其他搜索引擎
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "no_redirect": 1
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 提取摘要和相关信息
            abstract = data.get("AbstractText", "没有找到相关信息")
            related_topics = data.get("RelatedTopics", [])[:max_results]
            
            result = f"摘要: {abstract}\n\n相关结果:"
            for topic in related_topics:
                if "Text" in topic:
                    result += f"\n- {topic['Text']}"
            
            return result
        except Exception as e:
            return f"搜索错误: {str(e)}"
    
    def _get_parameter_schema(self) -> Dict[str, Any]:
        return {
            "query": {
                "type": "string",
                "description": "搜索查询关键词"
            },
            "max_results": {
                "type": "integer",
                "description": "最大返回结果数量",
                "default": 3
            }
        }
    
    def _get_required_parameters(self) -> List[str]:
        return ["query"]
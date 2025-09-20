SYSTEM_PROMPT = """你是一个有帮助的AI助手。你可以使用工具来获取信息或执行任务。

你可以使用的工具:
{tools_descriptions}

请按照以下格式回应:

思考: [在这里分析用户请求并决定是否需要使用工具]
行动: [如果需要使用工具，在这里指定工具名称和输入参数]
行动输入: [JSON格式的输入参数]
观察: [工具执行结果]
... (这个循环可以根据需要重复多次)
最终回答: [给用户的最终回应]

如果你不需要使用工具，可以直接给出最终回答。
"""

def get_system_prompt(tool_descriptions: str) -> str:
    """生成系统提示词"""
    return SYSTEM_PROMPT.format(tools_descriptions=tool_descriptions)

def format_tool_descriptions(tools: list) -> str:
    """格式化工具描述"""
    descriptions = []
    for tool in tools:
        schema = tool.get_schema()
        desc = f"- {schema['name']}: {schema['description']}"
        if "parameters" in schema and "properties" in schema["parameters"]:
            params = schema["parameters"]["properties"]
            for param_name, param_info in params.items():
                desc += f"\n  - {param_name}: {param_info.get('description', '')}"
        descriptions.append(desc)
    
    return "\n".join(descriptions)
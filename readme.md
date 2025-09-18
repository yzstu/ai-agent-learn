# AI Agent Learn

AI Agent Learn 是一个基于 `langchain` 的智能代理项目，旨在通过集成语言模型和工具链，帮助用户高效完成任务。

## 项目简介

本项目使用 `langchain_core` 提供的语言模型和提示模板，构建了一个可扩展的智能代理类 `MyAgent`。通过传入语言模型和工具列表，用户可以轻松实现任务的自动化处理。

## 功能特点

- **语言模型集成**：支持 Hugging Face 等主流语言模型。
- **工具链扩展**：可根据需求自定义工具列表。
- **灵活任务处理**：通过任务描述动态调用工具或生成答案。

## 使用方法

1. 初始化 `MyAgent`：
   ```python
   from core import MyAgent
   from langchain_core.language_models import SomeChatModel

   llm = SomeChatModel()
   tools = []  # 自定义工具列表
   agent = MyAgent(llm, tools)
   ```

2. 执行任务：
   ```python
   task_description = "帮我总结这段文字"
   response = agent.run(task_description)
   print(response)
   ```

3. 配置国内源（可选）：
   ```python
   agent.configure_download(proxy="http://127.0.0.1:7890", mirror_url="https://mirror.example.com/huggingface")
   ```

## 项目进度

- [x] 基础框架搭建
- [x] 集成语言模型
- [ ] 工具链扩展
- [ ] 增加更多任务处理逻辑
- [ ] 编写测试用例

## 贡献指南

欢迎对本项目提出建议或贡献代码！请提交 Pull Request 或创建 Issue。

## 许可证

本项目采用 [MIT License](LICENSE) 开源。
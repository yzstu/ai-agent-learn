import argparse
from core.agent import AIAgent

def main():
    parser = argparse.ArgumentParser(description="AI Agent with tool calling and memory")
    parser.add_argument("--model", choices=["siliconflow", "ollama"], default="ollama",
                       help="选择使用的模型 (默认: ollama)")
    
    args = parser.parse_args()
    
    # 初始化Agent
    agent = AIAgent()
    agent.set_model(args.model)
    
    print("AI Agent 已启动! 输入 'quit' 退出, 'clear' 清空对话历史")
    print(f"当前模型: {args.model}")
    
    while True:
        try:
            user_input = input("\n用户: ")
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                agent.short_term_memory.clear()
                print("对话历史已清空")
                continue
            
            response = agent.process_message(user_input)
            print(f"\n助手: {response}")
            
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
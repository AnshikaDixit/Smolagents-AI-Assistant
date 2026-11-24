import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel

# 1. Load environment variables
load_dotenv(".env.dev")

# 2. Configure Groq LLM
model = OpenAIServerModel(
    model_id="qwen/qwen3.8-27b",
    api_base="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
)

# 3. Run CodeAgent using local Docker container sandbox
# Requires Docker Desktop to be open and running on your machine.
if __name__ == "__main__":
    print("Spinning up local Docker container for CodeAgent...")
    with CodeAgent(
        model=model,
        tools=[],
        executor_type="docker",
    ) as agent:
        result = agent.run("Can you give me the 100th Fibonacci number?")
        print(f"\nFinal Result: {result}")

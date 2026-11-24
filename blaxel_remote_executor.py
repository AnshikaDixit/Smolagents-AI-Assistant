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

# 3. Remote Cloud Execution with Blaxel
# The `with ... as agent:` context manager spins up a dedicated Linux cloud container,
# installs required dependencies, runs the agent's code in the cloud,
# and terminates/deletes the container when finished.
if __name__ == "__main__":
    print("Connecting to Blaxel remote cloud sandbox...")
    with CodeAgent(
        model=model,
        tools=[],
        executor_type="blaxel",
    ) as agent:
        result = agent.run("Can you give me the 100th Fibonacci number?")
        print(f"\nFinal Result: {result}")

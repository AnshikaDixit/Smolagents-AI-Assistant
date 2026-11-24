import os
from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIServerModel

# 1. Load environment variables (API keys)
load_dotenv(".env.dev")

# 2. Configure Groq LLM (Fast & Free Brain)
model = OpenAIServerModel(
    model_id="qwen/qwen3.8-27b",
    api_base="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
)

if __name__ == "__main__":
    task = "What's the 20th Fibonacci number?"
    print(f"Task for Manager Agent: {task}\n")
    print("Spinning up Blaxel cloud sandbox for Coder Agent...")

    # 3. Specialist Worker Agent (Coder) using remote Blaxel cloud sandbox
    # The coder agent writes code and executes it in an isolated Blaxel container.
    with CodeAgent(
        model=model,
        tools=[],
        executor_type="blaxel",
        name="coder_agent",
        description="An expert software engineer agent that solves difficult mathematical and algorithmic problems using Python code inside a secure Blaxel cloud sandbox.",
    ) as coder_agent:

        # 4. Manager Agent (Boss): Plans tasks and delegates execution to the coder agent
        manager_agent = CodeAgent(
            model=model,
            tools=[],
            managed_agents=[coder_agent],
        )

        # 5. Run the Multi-Agent system
        response = manager_agent.run(task)
        print(f"\nFinal Result from Multi-Agent System: {response}")

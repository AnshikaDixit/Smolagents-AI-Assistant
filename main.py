import os
from dotenv import load_dotenv
from image_tool import image_generation_tool
from model_download_tool import model_download_tool
from smolagents import CodeAgent, OpenAIServerModel, GradioUI

# 1. Load environment variables
load_dotenv(".env.dev")

# 2. Configure the LLM Brain (Groq - fast & free)
model = OpenAIServerModel(
    model_id="qwen/qwen3.8-27b",
    api_base="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
)

# 3. Assemble the Agent with tools & guardrails
agent = CodeAgent(
    tools=[
        image_generation_tool,
        model_download_tool,
    ],
    model=model,
    max_steps=5,            # Guardrail: prevents runaway retry loops
    add_base_tools=True,    # Includes web_search, visit_webpage & Python utilities
)

# 4. Launch interactive Web UI
if __name__ == "__main__":
    print("Launching Smolagents Web UI...")
    GradioUI(agent).launch(share=False)

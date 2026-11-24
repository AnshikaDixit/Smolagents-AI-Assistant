import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# 1. Load environment variables
load_dotenv(".env.dev")

def run_code_raise_errors(sandbox, code: str, verbose: bool = False) -> str:
    execution = sandbox.run_code(
        code,
        envs={
            "HF_TOKEN": os.getenv("HF_TOKEN", ""),
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
        },
    )
    if execution.error:
        execution_logs = "\n".join([str(log) for log in execution.logs.stdout])
        logs = execution_logs + "\n" + execution.error.traceback
        raise ValueError(logs)
    return "\n".join([str(log) for log in execution.logs.stdout])

# 2. Define the multi-agent code to execute inside E2B
# Note: You can use InferenceClientModel or OpenAIServerModel (Groq)
agent_code = """
import os
from smolagents import CodeAgent, InferenceClientModel

# Initialize the coder agent (Worker)
agent = CodeAgent(
    model=InferenceClientModel(token=os.getenv("HF_TOKEN"), provider="together"),
    tools=[],
    name="coder_agent",
    description="This agent takes care of your difficult algorithmic problems using code."
)

# Initialize the manager agent (Boss)
manager_agent = CodeAgent(
    model=InferenceClientModel(token=os.getenv("HF_TOKEN"), provider="together"),
    tools=[],
    managed_agents=[agent],
)

# Run the multi-agent system
response = manager_agent.run("What's the 20th Fibonacci number?")
print(response)
"""

if __name__ == "__main__":
    print("Initializing E2B Sandbox...")
    # Using context manager ensures the E2B sandbox is cleaned up when finished
    with Sandbox() as sandbox:
        print("Installing smolagents inside E2B sandbox...")
        sandbox.commands.run("pip install smolagents")

        print("Executing multi-agent code in E2B sandbox...")
        execution_logs = run_code_raise_errors(sandbox, agent_code)
        print("\n--- Execution Logs ---")
        print(execution_logs)

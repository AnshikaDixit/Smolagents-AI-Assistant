import os
from typing import Optional
from dotenv import load_dotenv
import docker

# Load environment variables
load_dotenv(".env.dev")

class DockerSandbox:
    """
    Custom hardened Docker Sandbox for executing agent code with resource limits
    and dropped OS capabilities.
    """
    def __init__(self):
        self.client = docker.from_env()
        self.container = None

    def create_container(self):
        print("Building hardened Docker image 'agent-sandbox' from Dockerfile...")
        try:
            image, build_logs = self.client.images.build(
                path=".",
                tag="agent-sandbox",
                rm=True,
                forcerm=True,
                buildargs={},
            )
            print("Docker image 'agent-sandbox' built successfully.")
        except docker.errors.BuildError as e:
            print("Build error logs:")
            for log in e.build_log:
                if "stream" in log:
                    print(log["stream"].strip())
            raise

        print("Starting isolated Docker container with security constraints...")
        # Create container with strict security constraints
        self.container = self.client.containers.run(
            "agent-sandbox",
            command="tail -f /dev/null",  # Keep container running
            detach=True,
            tty=True,
            mem_limit="512m",             # RAM limit
            cpu_quota=50000,              # CPU limit (50% of 1 core)
            pids_limit=100,               # Prevent fork bombs
            security_opt=["no-new-privileges"],
            cap_drop=["ALL"],             # Drop all Linux root capabilities
            environment={
                "HF_TOKEN": os.getenv("HF_TOKEN", ""),
                "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
            },
        )
        print("Sandbox container running.")

    def run_code(self, code: str) -> Optional[str]:
        if not self.container:
            self.create_container()

        print("Executing agent code inside container as unprivileged user 'nobody'...")
        exec_result = self.container.exec_run(
            cmd=["python", "-c", code],
            user="nobody",
        )
        return exec_result.output.decode() if exec_result.output else None

    def cleanup(self):
        if self.container:
            print("Stopping and cleaning up sandbox container...")
            try:
                self.container.stop()
                self.container.remove()
            except docker.errors.NotFound:
                pass
            except Exception as e:
                print(f"Error during cleanup: {e}")
            finally:
                self.container = None
                print("Cleanup complete.")

if __name__ == "__main__":
    sandbox = DockerSandbox()

    # Agent code that will run inside the Docker container
    agent_code = """
import os
from smolagents import CodeAgent, OpenAIServerModel

# Using Groq model inside the container
model = OpenAIServerModel(
    model_id="qwen/qwen3.8-27b",
    api_base="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

agent = CodeAgent(model=model, tools=[])
response = agent.run("What's the 20th Fibonacci number?")
print(f"\\nResult from Docker Sandbox: {response}")
"""

    try:
        output = sandbox.run_code(agent_code)
        print("\n--- Container Output ---")
        print(output)
    finally:
        sandbox.cleanup()

# Smolagents AI Assistant

An intelligent, multi-tool AI agent built using Hugging Face's **`smolagents`** framework. It leverages a **`CodeAgent`** architecture powered by **Groq LPU** inference for ultra-fast, cost-free reasoning and code execution.

---

## 🚀 What This Project Does

Unlike standard conversational chatbots that simply generate text, this agent uses the **ReAct (Reason + Act)** pattern to solve tasks by writing, executing, and validating real Python code across different sandboxed environments.

### Core Capabilities:
1. **Mathematical & Algorithmic Problem Solving:**
   - Writes and executes Python code on the fly without hallucinating calculations.
2. **AI Image Generation (100% Free):**
   - Generates photorealistic and artistic images from text prompts using the state-of-the-art **`FLUX.1-schnell`** model via Hugging Face Spaces.
3. **Hugging Face Hub Model Discovery:**
   - Queries the live Hugging Face Hub API to find the most downloaded machine learning models across task categories (e.g., `text-to-video`, `text-classification`, `translation`).
4. **Web Search & Browsing:**
   - Built-in live web search and page visiting for real-time information retrieval.
5. **Interactive Web Interface:**
   - Provides a local **Gradio UI** web chat interface for natural conversation and rich media output.
6. **Multi-Agent Management:**
   - Supports orchestrating hierarchical Multi-Agent setups (e.g., Manager Agent delegating to specialized Worker Agents).
7. **Multiple Sandboxed Execution Environments:**
   - Supports **Local AST Sandboxing**, **Blaxel Cloud Containers**, and **E2B Code Interpreter Sandboxes**.

---

## 🏗️ Architecture Overview

```
User Prompt (via Gradio Web UI / CLI)
               │
               ▼
┌───────────────────────────────┐
│     smolagents CodeAgent      │
│  - ReAct planning loop        │
│  - Python code generation     │
└──────────────┬────────────────┘
               │
      ┌────────┴────────┬──────────────────────────────────────────┐
      ▼                 ▼                                          ▼
┌──────────────┐  ┌────────────────────────┐  ┌──────────────────────────────────────────┐
│  LLM Brain   │  │        Toolbox         │  │          Execution Sandboxes             │
│  Groq LPU    │  │ • image_generation     │  │ 1. Local AST Sandbox (LocalPython)       │
│ (Qwen 27B)   │  │ • model_download       │  │ 2. Remote Blaxel Cloud Container         │
└──────────────┘  │ • web_search & webpage │  │ 3. Remote E2B Code Interpreter Sandbox   │
                  └────────────────────────┘  └──────────────────────────────────────────┘
```

- **LLM Engine:** Hosted on Groq (`qwen/qwen3.8-27b`) via `OpenAIServerModel` for sub-second reasoning and code generation.
- **Image Offloading:** Image synthesis is offloaded to Hugging Face Zero-GPU spaces, avoiding heavy local GPU load and cloud API costs.
- **Guardrails:** Equipped with `max_steps=5` to prevent infinite loops and conserve API token quotas.

---

## 🔒 Code Execution Sandboxes

Allowing an LLM to generate and run Python code comes with significant security considerations. This project demonstrates all 3 execution models supported by `smolagents`:

### 1. Local AST Sandbox (`LocalPythonExecutor`)
Runs locally on your machine using an AST-based parser that restricts execution without using unsafe Python `eval()` or `exec()`.
* **Script:** [`custom_executor_safeguard.py`](custom_executor_safeguard.py)
* **Safeguards:** Blocks shell syntax (`!echo`), restricts unauthorized modules (`os`, `sys`, `subprocess`), detects backdoor access (`random._os`), and terminates infinite loops after 1M operations.

### 2. Remote Cloud Sandbox — Blaxel (`BlaxelExecutor`)
Runs code in an isolated, disposable Linux cloud container powered by [Blaxel](https://blaxel.ai).
* **Script:** [`blaxel_remote_executor.py`](blaxel_remote_executor.py)
* **Key Feature:** Dynamic cloud container provisioning via `executor_type="blaxel"`, automatic package installation, and automatic teardown upon exit.

### 3. Local Docker Container (`DockerExecutor`)
Runs code locally inside an isolated Docker container on your machine using Docker Desktop.
* **Script:** [`docker_executor.py`](docker_executor.py)
* **Key Feature:** Complete local isolation via `executor_type="docker"` without needing third-party cloud APIs. Requires Docker Desktop running.

### 4. Remote Cloud Sandbox — E2B Code Interpreter (`Sandbox`)
Runs an entire multi-agent hierarchy inside a remote Jupyter cloud container powered by [E2B](https://e2b.dev).
* **Script:** [`e2b_remote_executor.py`](e2b_remote_executor.py)
* **Key Feature:** Demonstrates a **Manager Agent** delegating tasks to a specialized **Coder Agent** inside an isolated E2B cloud sandbox.

---

## 📁 Project Structure

```
smolagents/
├── main.py                       # Main interactive Gradio AI Assistant with tools
├── multi_agent_manager.py        # Multi-Agent Manager + Coder Worker (Blaxel Cloud Sandbox)
├── blaxel_remote_executor.py     # Remote Cloud Sandbox execution demo (Blaxel)
├── docker_executor.py            # Built-in Docker Container execution (smolagents)
├── custom_docker_sandbox.py      # Hardened Custom Docker Sandbox (Resource limits & unprivileged user)
├── Dockerfile                    # Container definition for custom Docker sandbox
├── e2b_remote_executor.py        # Remote Code Interpreter & Multi-Agent demo (E2B)
├── custom_executor_safeguard.py  # Local AST Sandbox security safeguards demo
├── image_tool.py                 # Custom tool: FLUX.1-schnell image generator
├── model_download_tool.py        # Custom tool: Hugging Face model discovery
├── .env.dev                      # Environment variables & API keys (git-ignored)
├── .env.example                  # Template for required environment variables
├── .vscode/
│   └── settings.json             # Editor Python interpreter configuration
└── README.md                     # Project documentation
```

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ and a virtual environment set up:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install smolagents python-dotenv openai gradio-client huggingface-hub pillow ddgs blaxel e2b-code-interpreter
```

### 3. Configure Environment Variables
Create your `.env.dev` file with your credentials (see `.env.example`):
```env
# Hugging Face Access Token (https://huggingface.co/settings/tokens)
HF_TOKEN="hf_your_huggingface_token"

# Groq API Key (https://console.groq.com/keys)
GROQ_API_KEY="gsk_your_groq_api_key"

# Blaxel Cloud Sandbox (https://blaxel.ai) - optional
BL_API_KEY="bl_your_blaxel_api_key"
BL_WORKSPACE="your_blaxel_workspace_name"

# E2B Sandbox API Key (https://e2b.dev) - optional
E2B_API_KEY="e2b_your_api_key"
```

---

## 💻 Running the Project

### Option A: Interactive Web UI (Full Agent with Tools)
Start the Gradio web assistant:
```bash
python3 main.py
```
Open your browser at `http://127.0.0.1:7860`.

### Option B: Remote Cloud Sandbox Execution (Blaxel)
Execute code in an isolated Blaxel cloud container:
```bash
python3 blaxel_remote_executor.py
```

### Option C: Remote Code Interpreter & Multi-Agent (E2B)
Execute a Manager + Coder multi-agent setup in an E2B sandbox:
```bash
python3 e2b_remote_executor.py
```

### Option D: Local Sandbox Safeguards Test
Test local AST security guards (blocked imports, infinite loop protection):
```bash
python3 custom_executor_safeguard.py
```

### Option E: Multi-Agent Manager Hierarchy in Blaxel Cloud Sandbox
Run a Manager Agent delegating algorithmic tasks to a specialized Coder Agent executing in an isolated Blaxel cloud sandbox:
```bash
python3 multi_agent_manager.py
```

### Option F: Built-in Docker Container Sandbox
Execute code in an isolated local Docker container managed by smolagents:
```bash
python3 docker_executor.py
```

### Option G: Custom Hardened Docker Sandbox
Build and run a custom, hardened Docker container with memory/CPU limits and unprivileged user (`nobody`):
```bash
python3 custom_docker_sandbox.py
```

---

## 🌐 Hub Deployment
This agent has also been packaged and published to the Hugging Face Hub:
👉 **[huggingface.co/spaces/dixitanshika09/flux-image-agent](https://huggingface.co/spaces/dixitanshika09/flux-image-agent)**

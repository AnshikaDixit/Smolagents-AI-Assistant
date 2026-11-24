# Smolagents AI Assistant

An intelligent, multi-tool AI agent built using Hugging Face's **`smolagents`** framework. It leverages a **`CodeAgent`** architecture powered by **Groq LPU** inference for ultra-fast, cost-free reasoning and code execution.

---

## 🚀 What This Project Does

Unlike standard conversational chatbots that simply generate text, this agent uses the **ReAct (Reason + Act)** pattern to solve tasks by writing, executing, and validating real Python code in secure sandboxes.

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
6. **Dual Execution Modes:**
   - Supports both **Local AST Sandboxing** and **Remote Cloud Sandboxing** (via Blaxel).

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
      ┌────────┴────────┬─────────────────────────────┐
      ▼                 ▼                             ▼
┌──────────────┐  ┌────────────────────────┐  ┌─────────────────────────────────┐
│  LLM Brain   │  │        Toolbox         │  │     Code Execution Engine       │
│  Groq LPU    │  │ • image_generation     │  │ 1. Local AST Sandbox            │
│ (Qwen 27B)   │  │ • model_download       │  │    (LocalPythonExecutor)        │
└──────────────┘  │ • web_search & webpage │  │ 2. Remote Cloud Sandbox         │
                  └────────────────────────┘  │    (Blaxel Container)           │
                                              └─────────────────────────────────┘
```

- **LLM Engine:** Hosted on Groq (`qwen/qwen3.8-27b`) via `OpenAIServerModel` for sub-second reasoning and code generation.
- **Image Offloading:** Image synthesis is offloaded to Hugging Face Zero-GPU spaces, avoiding heavy local GPU load and cloud API costs.
- **Guardrails:** Equipped with `max_steps=5` to prevent infinite loops and conserve API token quotas.

---

## 🔒 Code Execution Sandboxes

Allowing an LLM to generate and run Python code comes with significant security considerations. This project demonstrates both execution models supported by `smolagents`:

### 1. Local AST Sandbox (`LocalPythonExecutor`)
Runs locally on your machine using an AST-based parser that restricts execution without using unsafe Python `eval()` or `exec()`.
* **Demonstrated in:** [`custom_executor_safeguard.py`](custom_executor_safeguard.py)
* **Safeguards:** Blocks shell syntax (`!echo`), restricts unauthorized modules (`os`, `sys`, `subprocess`), detects backdoor access (`random._os`), and terminates infinite loops after 1M operations.

### 2. Remote Cloud Sandbox (`BlaxelExecutor`)
Runs code **completely off your machine** inside a disposable, isolated Linux cloud container powered by [Blaxel](https://blaxel.ai).
* **Demonstrated in:** [`blaxel_remote_executor.py`](blaxel_remote_executor.py)
* **How it works:**
  - When invoked with `with CodeAgent(..., executor_type="blaxel") as agent:`, a dedicated remote cloud container is dynamically provisioned.
  - Automatically installs required dependencies (e.g. `numpy`, `pillow`) inside the remote container.
  - Executes code through a secure remote Jupyter kernel websocket.
  - **Zero Local Risk:** Dangerous or rogue code cannot harm your local files.
  - **Automatic Cleanup:** When finished, the container is safely terminated and deleted.

---

## 📁 Project Structure

```
smolagents/
├── main.py                       # Main interactive Gradio AI Assistant with tools
├── blaxel_remote_executor.py     # Remote Cloud Sandbox execution demo (Blaxel)
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
pip install smolagents python-dotenv openai gradio-client huggingface-hub pillow ddgs blaxel
```

### 3. Configure Environment Variables
Create your `.env.dev` file with your credentials (see `.env.example`):
```env
# Hugging Face Access Token (https://huggingface.co/settings/tokens)
HF_TOKEN="hf_your_huggingface_token"

# Groq API Key (https://console.groq.com/keys)
GROQ_API_KEY="gsk_your_groq_api_key"

# Blaxel Cloud Sandbox Credentials (https://blaxel.ai) - optional, for remote sandboxing
BL_API_KEY="bl_your_blaxel_api_key"
BL_WORKSPACE="your_blaxel_workspace_name"
```

---

## 💻 Running the Project

### Option A: Interactive Web UI (Full Agent with Tools)
Start the Gradio web assistant:
```bash
python3 main.py
```
Open your browser at `http://127.0.0.1:7860` to chat with the agent, generate images, search Hugging Face models, or browse the web.

### Option B: Remote Cloud Sandbox Execution (Blaxel)
Execute code in an isolated Blaxel cloud container:
```bash
python3 blaxel_remote_executor.py
```

### Option C: Local Sandbox Safeguards Test
Test local AST security guards (blocked imports, infinite loop protection):
```bash
python3 custom_executor_safeguard.py
```

---

## 🌐 Hub Deployment
This agent has also been packaged and published to the Hugging Face Hub:
👉 **[huggingface.co/spaces/dixitanshika09/flux-image-agent](https://huggingface.co/spaces/dixitanshika09/flux-image-agent)**

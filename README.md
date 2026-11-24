# Smolagents AI Assistant

An intelligent, multi-tool AI agent built using Hugging Face's **`smolagents`** framework. It leverages a **`CodeAgent`** architecture powered by **Groq LPU** inference for ultra-fast, cost-free reasoning and code execution.

---

## 🚀 What This Project Does

Unlike standard conversational chatbots that simply generate text, this agent uses the **ReAct (Reason + Act)** pattern to solve tasks by writing, executing, and validating real Python code in a secure local sandbox.

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

---

## 🏗️ Architecture Overview

```
User Prompt (via Gradio Web UI)
               │
               ▼
┌───────────────────────────────┐
│     smolagents CodeAgent      │
│  - ReAct planning loop        │
│  - Python code generation     │
│  - Sandboxed code execution   │
└──────────────┬────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────────┐  ┌────────────────────────────────────────┐
│  LLM Brain   │  │              Toolbox                   │
│  Groq LPU    │  │  • image_generation_tool (FLUX.1)      │
│ (Qwen 27B)   │  │  • model_download_tool (HF Hub API)   │
└──────────────┘  │  • web_search & visit_webpage          │
                  └────────────────────────────────────────┘
```

- **LLM Engine:** Hosted on Groq (`qwen/qwen3.8-27b`) via `OpenAIServerModel` for sub-second reasoning and code generation.
- **Image Offloading:** Image synthesis is offloaded to Hugging Face Zero-GPU spaces, avoiding heavy local GPU load and cloud API costs.
- **Guardrails:** Equipped with `max_steps=5` to prevent infinite loops and conserve API token quotas.

---

## 📁 Project Structure

```
smolagents/
├── main.py                 # Main entrypoint: Agent setup & Gradio UI launcher
├── image_tool.py           # Custom tool: FLUX.1-schnell image generator
├── model_download_tool.py  # Custom tool: Hugging Face model search
├── .env.dev                # Environment variables (API keys)
├── .vscode/
│   └── settings.json       # Editor Python interpreter configuration
└── README.md               # Project documentation
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
pip install smolagents python-dotenv openai gradio-client huggingface-hub pillow ddgs
```

### 3. Configure Environment Variables
Create or update your `.env.dev` file with your API keys:
```env
HF_TOKEN="hf_your_huggingface_token"
GROQ_API_KEY="gsk_your_groq_api_key"
```
> **Notes:**
> - Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys).
> - Get a free Hugging Face token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

---

## 💻 Running the Agent

Start the interactive Gradio web application:
```bash
python3 main.py
```

Open your browser and navigate to:
```
http://127.0.0.1:7860
```

### Example Prompts to Try:
- *"Calculate the 118th number in the Fibonacci sequence."*
- *"Generate an image of a smiling child playing in autumn leaves."*
- *"Which model has the most downloads in the 'text-to-video' task on Hugging Face?"*
- *"Search the web and tell me who the current CEO of Reliance Industries is."*

---

## 🌐 Hub Deployment
This agent has also been packaged and published to the Hugging Face Hub:
👉 **[huggingface.co/spaces/dixitanshika09/flux-image-agent](https://huggingface.co/spaces/dixitanshika09/flux-image-agent)**

from huggingface_hub import list_models
from smolagents import tool

@tool
def model_download_tool(task: str) -> str:
    """
    Returns the name of the most downloaded model for a given task on the Hugging Face Hub.

    Args:
        task: The machine learning task category (e.g. 'text-to-video', 'text-classification', 'translation').
    """
    try:
        # In huggingface_hub, sort="downloads" sorts in descending order by default
        most_downloaded_model = next(iter(list_models(filter=task, sort="downloads")))
        return most_downloaded_model.id
    except StopIteration:
        return f"No models found for task '{task}'."
    except Exception as e:
        return f"Error fetching models for task '{task}': {e}"

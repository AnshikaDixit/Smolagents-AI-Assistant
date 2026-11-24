from PIL import Image
from smolagents import tool

@tool
def image_generation_tool(prompt: str) -> Image.Image:
    """
    Generates an image from a text description using FLUX.1-schnell on Hugging Face Spaces for free.

    Args:
        prompt: A detailed description of the image to generate (e.g. 'a cute smiling golden retriever puppy, 4k').
    """
    import os
    # pyrefly: ignore[missing-import]
    from gradio_client import Client  # type: ignore
    from PIL import Image

    try:
        client = Client("black-forest-labs/FLUX.1-schnell", token=os.getenv("HF_TOKEN"))
        result = client.predict(
            prompt=prompt,
            seed=0,
            randomize_seed=True,
            width=512,
            height=512,
            num_inference_steps=4,
            api_name="/infer",
        )
        image_path = result[0]
        return Image.open(image_path)
    except Exception as e:
        raise RuntimeError(f"Image generation failed: {e}")

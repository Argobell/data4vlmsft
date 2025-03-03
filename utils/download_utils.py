from datasets import load_dataset
from PIL import Image
import os
from typing import Dict

def download_image_from_dataset(dataset, index, save_dir):
    """
    Download an image and text from the dataset to a local directory.
    Args:
        dataset (Dataset): The Hugging Face Dataset object.
        index (int): The index of the data item to process.
        save_dir (str): The directory where the image will be saved.
    Returns:
        Dict with 'path' and 'text' fields.
    """
    os.makedirs(save_dir, exist_ok=True)
    item = dataset[index]
    image = item['image']
    text = item['text']
    image = image.convert('L')  
    filename = f"image_{index}.jpg"
    image_path = os.path.join(save_dir, filename)
    image.save(image_path, quality=95)
    return {
        'path': image_path, 
        'text': text
    }

from datasets import Dataset, Image
from PIL import Image as PILImage
import os
import pyarrow

def create_hf_dataset_from_txt(image_folder, label_path, output_path):
    """
    Create a Hugging Face Dataset from a folder containing images and a TXT file with labels, converting the images to grayscale.

    Args:
        image_folder (str): Path to the folder containing the images.
        label_path (str): Path to the TXT file containing the filenames and corresponding labels.
                          Each line should be in the format "filename.jpg label text" (space-separated).
        output_path (str): Path where the dataset will be saved.

    Returns:
        Dataset: A Hugging Face Dataset object.
    """
    image_paths = []
    texts = []
    pil_images = []
    try:
        with open(label_path, 'r', encoding='utf-8') as f:  
            for line in f:
                parts = line.strip().split(' ', 1)  # Split at the first space
                if len(parts) == 2:
                    image_file_name = parts[0].strip()
                    text_label = parts[1].strip()
                    # Build the full image path
                    image_path = os.path.join(image_folder, image_file_name)
                    # Check if the image file exists
                    if not os.path.exists(image_path):
                        print(f"Warning: Image file not found: {image_path}. Skipping.")
                        continue
                    try:
                        img = PILImage.open(image_path).convert('L')  # 'L' for grayscale
                        pil_images.append(img)  # Save the PIL Image object
                        image_paths.append(image_path)  # Record the original path for debugging
                        texts.append(text_label)
                    except Exception as e:
                        print(f"Warning: Unable to open or convert image {image_path}: {e}. Skipping.")
                        continue

                else:
                    print(f"Warning: Malformed line: '{line.strip()}'. Skipping.")
    except FileNotFoundError:
        print(f"Error: Label file not found {label_path}.")
        return None
    except Exception as e:
        print(f"Error reading label file: {e}")
        return None
    if not image_paths:
        print("Error: No valid image files or labels found. Please check paths and file contents.")
        return None
    data = {
        'image': pil_images,  # Use PIL Image objects
        'text': texts
    }
    dataset = Dataset.from_dict(data)
    dataset = dataset.cast_column("image", Image())
    # Save the dataset to disk.
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)  # Create directory if it does not exist
        dataset.save_to_disk(output_path)
        print(f"Dataset saved to: {output_path}")
    except Exception as e:
        print(f"Error saving dataset: {e}")
        return None
    return dataset

# Example usage:
image_folder = "D:\\data4vlm\\hwe_dataset\\data_composition"  # <-- Replace with your image folder path
label_path = "D:\\data4vlm\\hwe_dataset\\label_10000.txt"  # <-- Replace with your label file path
output_path = "./hwe_dataset_gray"  # <-- Replace with the path where you want to save the dataset
hf_dataset = create_hf_dataset_from_txt(image_folder, label_path, output_path)
if hf_dataset:
    print(hf_dataset)
else:
    print("Failed to create Hugging Face Dataset. Please check error messages.")

import json
import os
import random
from typing import List, Dict, Any, Optional
from utils import random_instruction, convert2sharegpt, convert2conversation
from datasets import load_dataset

class DatasetBuilder:
    def __init__(self, dataset_path: str, save_dir: str):
        """
        Initialize the DatasetBuilder.

        Args:
            dataset_path (str): Path to the Hugging Face dataset.
            save_dir (str): Directory to save downloaded images.
            use_lf_format (bool): Whether to use the LF format for ShareGPT.
        """
        self.dataset_path = dataset_path
        self.save_dir = save_dir
        self.dataset = load_dataset(dataset_path, split='train')

    def download_image_from_dataset(self, dataset, index, save_dir):
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

    def build_dataset(self, num_samples: int,instructions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Build the ShareGPT format dataset.

        Args:
            num_samples (int): Number of samples to process.

        Returns:
            List[Dict[str, Any]]: List of ShareGPT format data.
        """
        num_rows=len(self.dataset)
        if num_samples > num_rows:
            num_samples = num_rows
        
        self.dataset = self.dataset.shuffle(seed=42).select(range(num_samples))

        sharegpt_data = []
        for i in range(num_samples):
            if instructions and len(instructions) > 0:
                instruction = random.choice(instructions)
            else:
                instruction = random_instruction()
            sample = self.download_image_from_dataset(self.dataset, i, self.save_dir)
            sharegpt_data.append(convert2sharegpt(sample, instruction))
        
        return sharegpt_data
    
    def save_dataset(self, sharegpt_data: List[Dict[str, Any]], output_path: str):
        """
        Save the ShareGPT format dataset to a JSON file.

        Args:
            sharegpt_data (List[Dict[str, Any]]): ShareGPT format data.
            output_path (str): Path to save the JSON file.
        """
        with open(output_path, 'w') as f:
            json.dump(sharegpt_data, f, indent=4)

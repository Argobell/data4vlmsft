import random

def random_instruction():
    instruction = [
        "Can you tell me what the handwritten text in the image says?",
        "What does the handwritten writing in the picture say?",
        "Could you identify the handwritten words in the photo?",
        "What is written by hand in the image?",
        "Can you read the handwritten English in the picture?",
        "What is the handwritten content in the image?",
        "Could you decipher the handwritten text in the picture?",
        "What does the handwritten note in the image say?",
        "Can you make out the handwritten words in the photo?",
        "What is the handwritten script in the picture?"
    ]
    return random.choice(instruction)
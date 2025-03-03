def convert2conversation(sample,instruction:str):
    conversation = [
        { "role": "user",
          "content" : [
            {"type" : "text",  "text"  : instruction},
            {"type" : "image", "image" : sample["image"]} ]
        },
        { "role" : "assistant",
          "content" : [
            {"type" : "text",  "text"  : sample["text"]} ]
        },
    ]
    return { "messages" : conversation }

def convert2sharegpt(sample,instruction:str):
    conversation = [
        { "role": "user",
          "content" : f"<image>{instruction}"
        },
        { "role" : "assistant",
          "content" : sample["text"]
        },
    ]
    images = [
        sample["path"]
    ]
    return { "messages" : conversation,"images": images }

        
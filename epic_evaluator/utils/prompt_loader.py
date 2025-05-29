import os

def load_prompt(filename):
    with open(os.path.join("prompts", filename), "r", encoding="utf-8") as file:
        return file.read()

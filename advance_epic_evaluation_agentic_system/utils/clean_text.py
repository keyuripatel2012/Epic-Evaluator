import regex as re

def clean_text(text):
    text = re.sub(r"\*{1,2}([^*]+?)\*{1,2}", r"\1", text)
    text = re.sub(r"[#]+", "", text)
    return text.strip()
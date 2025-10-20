from transformers import AutoTokenizer

def tokenize_text(text: str, model_name="bert-base-uncased"):
    """Tokenizes input text into model-compatible tokens."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    return tokens

def text_to_ids(text: str, model_name="bert-base-uncased"):
    """Converts text to token IDs for model input."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer(text, return_tensors="pt", truncation=True, padding=True)

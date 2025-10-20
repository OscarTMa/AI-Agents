from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoTokenizer
from datasets import load_dataset

def fine_tune_model(model_name="distilbert-base-uncased", dataset_name="imdb"):
    """Basic fine-tuning pipeline for sentiment classification."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dataset = load_dataset(dataset_name)
    
    def tokenize_fn(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length")
    
    tokenized = dataset.map(tokenize_fn, batched=True)
    
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        per_device_train_batch_size=8,
        num_train_epochs=1
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"].select(range(1000)),
        eval_dataset=tokenized["test"].select(range(500))
    )
    
    trainer.train()
    model.save_pretrained("./models/finetuned_model")

if __name__ == "__main__":
    fine_tune_model()

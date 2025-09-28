from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class ParaphraseConfig:
    def __init__(self, model_name="Vamsi/T5_Paraphrase_Paws", max_length=256, num_return_sequences=1, enabled=True):
        self.model_name = model_name
        self.max_length = max_length
        self.num_return_sequences = num_return_sequences
        self.enabled = enabled

class Paraphraser:
    def __init__(self, config: ParaphraseConfig = ParaphraseConfig()):
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(config.model_name)
        self.config = config

    def paraphrase(self, text: str) -> str:
        input_text = f"paraphrase: {text} </s>"
        encoding = self.tokenizer(
            input_text,
            padding="longest",
            max_length=self.config.max_length,
            truncation=True,
            return_tensors="pt"
        )
        with torch.no_grad():
            outputs = self.model.generate(
                encoding["input_ids"],
                max_length=self.config.max_length,
                num_return_sequences=self.config.num_return_sequences,
                num_beams=5,
                temperature=1.5
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from langchain.schema.runnable import RunnablePassthrough

class Phi2LLM:
    def __init__(self, model_name, tokenizer):
        self.model_name = model_name
        self.tokenizer = tokenizer
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def __call__(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt")["input_ids"]
        output = self.model.generate(input_ids, max_length=1024)
        return self.tokenizer.decode(output[0], skip_special_tokens=True).strip()

import os

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from config import SBERT_MODEL


class Worker:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            SBERT_MODEL, token=os.getenv("HF_TOKEN")
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            SBERT_MODEL,
            token=os.getenv("HF_TOKEN"),
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            cache_dir=os.getenv("TRANSFORMERS_CACHE"),
        )

    def answer(self, data):
        inputs = self.tokenizer.apply_chat_template(
            data.chat_history,
            return_dict=True,
            return_tensors="pt",
            add_generation_prompt=True,
        ).to(f"cuda:{os.getenv('NVIDIA_VISIBLE_DEVICES')}")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, max_new_tokens=data.max_new_tokens, do_sample=True
            )

        o = self.tokenizer.decode(outputs[0], skip_special_tokens=True).split(
            "assistant\n\n"
        )[-1]

        torch.cuda.empty_cache()

        return o


if __name__ == "__main__":
    w = Worker()

    r = w.answer([{"role": "user", "content": "Who are you?"}])
    print(r)

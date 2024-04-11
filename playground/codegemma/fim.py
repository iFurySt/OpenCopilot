import os
import time

from transformers import GemmaTokenizer, AutoModelForCausalLM

access_token = os.getenv("HF_TOKEN")
model_id = "google/codegemma-7b"

# gpu_device = os.getenv("CUDA_VISIBLE_DEVICE", "cuda:0")
# device = gpu_device if torch.cuda.is_available() else "cpu"
# model.to(device)

tokenizer = GemmaTokenizer.from_pretrained(model_id, token=access_token)
# export CUDA_VISIBLE_DEVICES=0,1
# use multiple devices if available
model = AutoModelForCausalLM.from_pretrained(
    model_id, token=access_token, device_map="auto"
)

prompt = '''\
<|fim_prefix|>import datetime
def calculate_age(birth_year):
    """Calculates a person's age based on their birth year."""
    current_year = datetime.date.today().year
    <|fim_suffix|>
    return age<|fim_middle|>\
'''

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
prompt_len = inputs["input_ids"].shape[-1]
ts = time.time()
outputs = model.generate(**inputs, max_new_tokens=100)
elapsed_sec = time.time() - ts
print(tokenizer.decode(outputs[0][prompt_len:]))
print(f"Elapsed time: {elapsed_sec:.3f} sec")

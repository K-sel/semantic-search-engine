from datasets import load_dataset
import os

os.makedirs("data", exist_ok=True)

ds = load_dataset(
    "debasishraychawdhuri/wikipedia_clean_5GB", split="train", streaming=True
)

target_docs = 1000
saved_count = 0
processed_count = 0
min_length = 500

for item in ds:
    processed_count += 1

    if "text" in item and item["text"] and len(item["text"].strip()) >= min_length:
        filename = f"data/wiki_{saved_count}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(item["text"])

        saved_count += 1

        if saved_count >= target_docs:
            break
    else:
        text_len = len(item.get("text", "").strip()) if item.get("text") else 0

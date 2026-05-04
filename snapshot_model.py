"""
download_model.py
-----------------
Downloads paraphrase-multilingual-MiniLM-L12-v2 to ./models/minilm

Usage:
    python download_model.py
"""

from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    local_dir="./models/minilm",
    ignore_patterns=[
        "pytorch_model.bin",
        "tf_model.h5",
        "onnx/*",
        "openvino/*",
        "flax_model.msgpack",
        "rust_model.ot",
    ],
)

print("Done. Model saved to ./models/minilm")

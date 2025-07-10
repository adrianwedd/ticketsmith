# Local Inference with llama-cpp-python

This guide shows how to run quantized GGUF models on your own machine using `llama-cpp-python`.

## Installation

### macOS (Apple Silicon)

Install the library with Metal acceleration:

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install --no-binary :all: llama-cpp-python
```

### Linux (CUDA)

Install with CUDA support by setting the appropriate CMake flags:

```bash
CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install --no-binary :all: llama-cpp-python
```

A CPU-only build can be installed with:

```bash
pip install llama-cpp-python
```

## Download Quantized GGUF Models

Quantized models are available on Hugging Face:

- [TheBloke/Llama-3-8B-Instruct-GGUF](https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF)
- [TheBloke/Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)

Download a `q4_0` or `q4_K_M` file and note its path.

## Example Script

```python
from llama_cpp import Llama

# Path to your downloaded GGUF model
MODEL_PATH = "./models/llama-3-8b-instruct.Q4_K_M.gguf"

def main() -> None:
    """Run a simple prompt against the local model."""
    llm = Llama(model_path=MODEL_PATH)
    response = llm("Hello, world!", max_tokens=32)
    print(response["choices"][0]["text"].strip())

if __name__ == "__main__":
    main()
```

Run the script with Python 3.11:

```bash
python3.11 scripts/local_inference.py
```

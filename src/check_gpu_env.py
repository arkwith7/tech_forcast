import sys
import importlib.util
import torch
import subprocess

def check_library(name, package_name=None):
    if package_name is None:
        package_name = name
    
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return f"❌ {name}: Not Installed"
    else:
        try:
            ver = importlib.metadata.version(package_name)
            return f"✅ {name}: Installed ({ver})"
        except:
            return f"✅ {name}: Installed (Version unknown)"

def check_system():
    print("=== 1. GPU Hardware Check (nvidia-smi) ===")
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("❌ nvidia-smi failed or not found. (No NVIDIA GPU detected or driver issue)")
            print(result.stderr)
    except FileNotFoundError:
        print("❌ nvidia-smi command not found.")

    print("\n=== 2. PyTorch CUDA Check ===")
    print(f"PyTorch Version: {torch.__version__}")
    if torch.cuda.is_available():
        print(f"✅ CUDA Available: Yes")
        print(f"✅ GPU Device Name: {torch.cuda.get_device_name(0)}")
        print(f"✅ GPU Count: {torch.cuda.device_count()}")
        print(f"✅ Current Device: {torch.cuda.current_device()}")
    else:
        print("❌ CUDA Available: No (Using CPU)")

    print("\n=== 3. Deep Learning Libraries Check ===")
    libs = {
        "BERTopic": "bertopic",
        "Transformers": "transformers",
        "Sentence-Transformers": "sentence_transformers",
        "UMAP": "umap",
        "HDBSCAN": "hdbscan"
    }
    
    for display_name, pkg_name in libs.items():
        print(check_library(display_name, pkg_name))

if __name__ == "__main__":
    check_system()


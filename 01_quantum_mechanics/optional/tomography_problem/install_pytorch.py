import os
import platform
import subprocess
import sys

def get_cuda_compute_capability():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=compute_cap', '--format=csv,noheader'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Taking the capability of the first GPU
            cap_str = result.stdout.strip().split('\n')[0]
            major, minor = map(int, cap_str.split('.'))
            return major, minor
    except FileNotFoundError:
        return None
    return None

def install(package_string):
    print(f"Running: pip install --no-cache-dir {package_string}")
    env = os.environ.copy()
    env["TMPDIR"] = os.getcwd()
    cmd = [sys.executable, "-m", "pip", "install", "--no-cache-dir"] + package_string.split()
    subprocess.check_call(cmd, env=env)

def main():
    print("="*60)
    print("Dynamic PyTorch Installer")
    print("="*60)
    
    os_name = platform.system()
    machine = platform.machine()
    
    if os_name == "Darwin" and machine == "arm64":
        print("Detected: Apple Silicon Mac")
        print("Installing the latest PyTorch for native MPS acceleration...")
        install("torch torchvision torchaudio")
    elif os_name in ["Linux", "Windows"]:
        cap = get_cuda_compute_capability()
        if cap is not None:
            major, minor = cap
            print(f"Detected: NVIDIA GPU with Compute Capability {major}.{minor}")
            if major < 7:
                print("Your GPU is older (sm_50 or sm_60 architecture).")
                print("Installing PyTorch 1.12.1 which still contains kernels for your GPU...")
                install("torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113")
            else:
                print("Your GPU supports modern PyTorch.")
                print("Installing the latest PyTorch with CUDA 12 support...")
                install("torch torchvision torchaudio")
        else:
            print("Detected: CPU only (No NVIDIA GPU found via nvidia-smi)")
            print("Installing the CPU-only version of PyTorch to save disk space...")
            install("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
    else:
        print(f"Detected: {os_name} {machine}")
        print("Falling back to default PyTorch installation...")
        install("torch torchvision torchaudio")
        
    print("="*60)
    print("Installation Complete!")
    print("="*60)

if __name__ == "__main__":
    main()

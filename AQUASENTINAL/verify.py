import subprocess
import sys
import os
from pathlib import Path

def run_cmd(cmd, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error ({result.returncode}):\n{result.stderr}")
        return False
    print("Success.")
    return True

def main():
    python_exe = os.path.join(".venv", "Scripts", "python.exe")
    pytest_exe = os.path.join(".venv", "Scripts", "pytest.exe")
    
    steps = [
        (f'"{python_exe}" src/data_generator.py', "Data Generation"),
        (f'"{python_exe}" src/train_model.py', "Model Training"),
        (f'"{python_exe}" -m pytest tests/', "Pytest"),
    ]
    
    for cmd, name in steps:
        if not run_cmd(cmd):
            print(f"Failed at {name}")
            sys.exit(1)
            
    print("All verification steps passed!")

if __name__ == "__main__":
    main()

import subprocess
import sys
import os

def run_script(script_path):
    """Executes a Python script and waits for its completion."""
    print(f"Running: {script_path}...")
    try:
        # Executes the script using the current system interpreter
        result = subprocess.run([sys.executable, script_path], check=True, text=True, capture_output=True)
        print(f"Success: {script_path}")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}:")
        print(e.stderr)
        sys.exit(1)

def main():
    print("="*50)
    print("CRYPTO SENTINEL: DATA PIPELINE STARTED")
    print("="*50)

    # Ordered pipeline following the Medallion Architecture
    pipeline = [
        "scripts/ingestion_bronze.py",
        "scripts/process_silver.py",
        "scripts/process_gold.py"
    ]

    for script in pipeline:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f"File not found: {script}")
            sys.exit(1)

    print("="*50)
    print("PIPELINE FINISHED SUCCESSFULLY!")
    print("GOLD data is ready for Power BI consumption.")
    print("="*50)

if __name__ == "__main__":
    main()
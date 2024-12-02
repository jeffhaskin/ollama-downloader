import subprocess
import sys
import time

def run_ollama_pull(model_name):
    """
    Pull an Ollama model and display raw output.
    Returns True if successful, False otherwise.
    """
    try:
        print(f"Now downloading {model_name}")
        
        process = subprocess.Popen(
            ['ollama', 'pull', model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        
        # Simply print whatever Ollama outputs
        while True:
            char = process.stdout.read(1)
            if char == '' and process.poll() is not None:
                break
            if char:
                print(char, end='', flush=True)
                
        return_code = process.poll()
        
        if return_code == 0:
            print(f"\n✅ Successfully downloaded {model_name}")
            return True
        else:
            print(f"\n❌ Failed to download {model_name}")
            return False
            
    except FileNotFoundError:
        print("\n❌ Error: Ollama is not installed or not in your PATH")
        print("Please install Ollama first: https://ollama.ai")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error while downloading {model_name}: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python OllamaDownloader.py \"model1,model2,model3\"")
        print("Example: python OllamaDownloader.py \"phi:latest,llama2:13b\"")
        sys.exit(1)
        
    # Split the comma-separated model names and remove any whitespace
    models = [model.strip() for model in sys.argv[1].split(',')]
    
    if not models:
        print("Error: No models specified")
        sys.exit(1)
        
    print(f"Starting sequential download of {len(models)} models...\n")
    
    for model in models:
        success = run_ollama_pull(model)
        if not success:
            print(f"\nStopping due to failure downloading {model}")
            sys.exit(1)
        
        if model != models[-1]:  # Don't wait after the last model
            print(f"\nWaiting 5 seconds before proceeding...")
            time.sleep(5)
    
    print("\n✨ All models downloaded successfully!")

if __name__ == "__main__":
    main()
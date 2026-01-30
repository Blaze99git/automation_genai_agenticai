import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import settings

def main():
    print("OpenAI Key Loaded:", bool(settings.OPENAI_API_KEY))
    print("Gemini Key Loaded:", bool(settings.GEMINI_API_KEY))
    print("Output Dir:", settings.OUTPUT_DIR)

if __name__ == "__main__":
    main()

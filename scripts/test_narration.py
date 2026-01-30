import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.narration_agent import NarrationAgent


def main():
    script_path = ROOT_DIR / "output" / "episodes" / "episode_1.txt"

    audio_dir = ROOT_DIR / "output" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    output_file = audio_dir / "episode_1.wav"

    agent = NarrationAgent()
    agent.run(script_path, output_file)

    print(f"Emotional narration saved to: {output_file}")


if __name__ == "__main__":
    main()

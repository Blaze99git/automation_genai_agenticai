import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.image_generation_agent import ImageGenerationAgent


def main():
    prompt_file = ROOT_DIR / "output/visuals/episode_1_prompts.json"
    output_dir = ROOT_DIR / "assets/visuals/backgrounds/episode_1"

    agent = ImageGenerationAgent()
    agent.run(prompt_file, output_dir)

    print(f"Images generated in {output_dir}")


if __name__ == "__main__":
    main()

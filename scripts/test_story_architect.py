import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.story_architect import StoryArchitectAgent


def main():
    agent = StoryArchitectAgent()

    result = agent.run(
        genre="Science Fiction",
        theme="A forgotten signal from deep space",
        episode_count=4,
        audience="YouTube sci-fi listeners"
    )

    output_dir = ROOT_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "story_blueprint.json"
    output_file.write_text(json.dumps(result, indent=2))

    print(f"Story blueprint saved to {output_file}")


if __name__ == "__main__":
    main()

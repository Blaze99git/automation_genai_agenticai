import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.visual_prompt_agent import VisualPromptAgent


def main():
    blueprint = json.loads(
        (ROOT_DIR / "output/story_blueprint.json").read_text()
    )

    script = (
        ROOT_DIR / "output/episodes/episode_1.txt"
    ).read_text()

    agent = VisualPromptAgent()
    result = agent.run(
        episode_number=1,
        metadata=blueprint,
        script=script
    )

    out_dir = ROOT_DIR / "output/visuals"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "episode_1_prompts.json"
    out_file.write_text(json.dumps(result, indent=2))

    print(f"Visual prompts saved to {out_file}")


if __name__ == "__main__":
    main()

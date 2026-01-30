import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.episode_writer import EpisodeWriterAgent


def main():
    blueprint_path = ROOT_DIR / "output" / "story_blueprint.json"
    blueprint = json.loads(blueprint_path.read_text())

    episode = blueprint["episodes"][0]  # Episode 1 only

    agent = EpisodeWriterAgent()
    script = agent.run(blueprint, episode)

    output_dir = ROOT_DIR / "output" / "episodes"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"episode_{episode['episode']}.txt"
    output_file.write_text(script)

    print(f"Episode script saved to {output_file}")


if __name__ == "__main__":
    main()

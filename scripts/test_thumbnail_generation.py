import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.thumbnail_agent import ThumbnailAgent


def main():
    episode_id = 1

    blueprint = json.loads(
        (ROOT_DIR / "output/story_blueprint.json").read_text()
    )

    title = blueprint["title"]

    backgrounds_dir = (
        ROOT_DIR / "assets" / "visuals" / "backgrounds" / "episode_1"
    )

    output_dir = ROOT_DIR / "assets" / "thumbnails"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"episode_{episode_id}.png"

    agent = ThumbnailAgent()
    agent.run(
        episode_id=episode_id,
        title=title,
        backgrounds_dir=backgrounds_dir,
        output_path=output_path,
    )

    print(f"Thumbnail created at {output_path}")


if __name__ == "__main__":
    main()

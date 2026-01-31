import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.video_assembly_agent import VideoAssemblyAgent


def main():
    episode_id = 1

    audio_path = ROOT_DIR / "output" / "audio" / "episode_1.wav"
    video_dir = ROOT_DIR / "output" / "video"
    video_dir.mkdir(parents=True, exist_ok=True)

    output_file = video_dir / "episode_1.mp4"

    agent = VideoAssemblyAgent(episode_id=episode_id)
    agent.run(audio_path, output_file)

    print(f"Video created at: {output_file}")


if __name__ == "__main__":
    main()

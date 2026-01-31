from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent

from moviepy import (
    AudioFileClip,
    ImageClip,
    CompositeAudioClip,
    concatenate_videoclips,
    concatenate_audioclips
)


class VideoAssemblyAgent(BaseAgent):
    def __init__(self, episode_id: int):
        super().__init__("VideoAssemblyAgent")

        self.episode_id = episode_id

        # ---- Video settings ----
        self.fps = 24
        self.resolution = (1920, 1080)
        self.image_duration = 8  # seconds per image

        # ---- Paths ----
        self.background_dir = Path(
            f"assets/visuals/backgrounds/episode_{episode_id}"
        )
        self.music_path = Path("assets/visuals/music/ambient_01.mp3")

        logger.info(f"Using backgrounds from {self.background_dir}")

        if not self.background_dir.exists():
            raise FileNotFoundError(
                f"Background images folder missing: {self.background_dir}"
            )

        if not self.music_path.exists():
            raise FileNotFoundError("Background music missing")

    # ----------------------------------
    # Ken Burns slow zoom (safe & light)
    # ----------------------------------
    def ken_burns(self, clip, zoom=1.08):
        return clip.resized(
            lambda t: 1 + (zoom - 1) * (t / clip.duration)
        )

    # ----------------------------------
    # Safe manual music looping (MoviePy v2)
    # ----------------------------------
    def build_looped_music(self, target_duration: float):
        base_music = AudioFileClip(str(self.music_path)).with_volume_scaled(0.18)

        clips = []
        total = 0.0

        while total < target_duration:
            clips.append(base_music)
            total += base_music.duration

        looped_music = concatenate_audioclips(clips)

        # MoviePy v2 uses subclipped()
        return looped_music.subclipped(0, target_duration)

    # ----------------------------------
    # Main assembly pipeline
    # ----------------------------------
    def run(self, narration_path: Path, output_path: Path):
        logger.info("Assembling cinematic video")

        if not narration_path.exists():
            raise FileNotFoundError(f"Narration not found: {narration_path}")

        narration = AudioFileClip(str(narration_path))
        duration = narration.duration

        logger.info(f"Narration duration: {duration:.2f}s")

        # ---- AUDIO ----
        music = self.build_looped_music(duration)
        final_audio = CompositeAudioClip([music, narration])

        # ---- VISUALS ----
        images = sorted(self.background_dir.glob("*"))
        if not images:
            raise RuntimeError("No background images found")

        clips = []
        elapsed = 0.0
        index = 0

        while elapsed < duration:
            img = images[index % len(images)]

            clip = (
                ImageClip(str(img))
                .resized(self.resolution)
                .with_duration(self.image_duration)
                .with_fps(self.fps)
            )

            clip = self.ken_burns(clip)
            clips.append(clip)

            elapsed += self.image_duration
            index += 1

        video = concatenate_videoclips(clips, method="compose")
        video = video.with_audio(final_audio)

        # ---- RENDER ----
        logger.info("Rendering cinematic video")

        video.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            fps=self.fps
        )

        logger.info(f"Cinematic video saved to {output_path}")

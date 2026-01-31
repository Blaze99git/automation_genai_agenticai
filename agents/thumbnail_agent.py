from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent
from PIL import Image, ImageDraw, ImageFont


class ThumbnailAgent(BaseAgent):
    def __init__(self):
        super().__init__("ThumbnailAgent")

        self.size = (1280, 720)
        self.font_size = 96

        # Try system font first
        self.font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not Path(self.font_path).exists():
            raise FileNotFoundError("Bold font not found on system")

    def run(
        self,
        episode_id: int,
        title: str,
        backgrounds_dir: Path,
        output_path: Path,
    ):
        logger.info(f"Generating thumbnail for episode {episode_id}")

        images = sorted(backgrounds_dir.glob("*"))
        if not images:
            raise RuntimeError("No background images found for thumbnail")

        # Pick the first image (later we can score images)
        bg_image = Image.open(images[0]).convert("RGB")
        bg_image = bg_image.resize(self.size)

        # Dark overlay for readability
        overlay = Image.new("RGBA", self.size, (0, 0, 0, 130))
        combined = Image.alpha_composite(bg_image.convert("RGBA"), overlay)

        draw = ImageDraw.Draw(combined)
        font = ImageFont.truetype(self.font_path, self.font_size)

        # Text positioning (bottom-left safe zone)
        margin_x = 60
        margin_y = self.size[1] - 200

        draw.text(
            (margin_x, margin_y),
            title,
            font=font,
            fill=(255, 255, 255),
        )

        combined.convert("RGB").save(output_path)
        logger.info(f"Thumbnail saved to {output_path}")

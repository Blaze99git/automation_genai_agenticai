import json
from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent

import torch
from diffusers import StableDiffusionXLPipeline


class ImageGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ImageGenerationAgent")

        self.device = "cpu"  # GPU later if available
        self.model_id = "stabilityai/sdxl-base-1.0"

        logger.info("Loading SDXL model (first time will be slow)")
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32
        )
        self.pipe = self.pipe.to(self.device)

        self.style_prefix = (
            "cinematic still from a science fiction film, "
            "ultra-detailed environment, dramatic lighting, "
            "high contrast, volumetric light, professional color grading, "
            "35mm lens, shallow depth of field, moody atmosphere, "
            "realistic textures, no text, no watermark, "
        )

    def run(self, prompt_file: Path, output_dir: Path):
        logger.info(f"Generating SDXL images from {prompt_file.name}")

        data = json.loads(prompt_file.read_text())
        prompts = data["prompts"]

        output_dir.mkdir(parents=True, exist_ok=True)

        for item in prompts:
            img_id = item["id"]
            base_prompt = item["description"]
            prompt = self.style_prefix + base_prompt

            logger.info(f"Generating image {img_id}")

            image = self.pipe(
                prompt=prompt,
                num_inference_steps=20,
                guidance_scale=7.0,
                height=720,
                width=1280,
                generator=torch.Generator(self.device).manual_seed(42)
            ).images[0]

            out_path = output_dir / f"bg_{img_id:03d}.png"
            image.save(out_path)

        logger.info("SDXL image generation complete")

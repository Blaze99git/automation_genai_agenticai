import json
from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent

import torch
from diffusers import StableDiffusionPipeline


class ImageGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ImageGenerationAgent")

        self.device = "cpu"  # CPU-first (safe)
        self.model_id = "runwayml/stable-diffusion-v1-5"

        logger.info("Loading Stable Diffusion model (this may take time)")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32
        )
        self.pipe = self.pipe.to(self.device)

    def run(self, prompt_file: Path, output_dir: Path):
        logger.info(f"Generating images from {prompt_file.name}")

        data = json.loads(prompt_file.read_text())
        prompts = data["prompts"]

        output_dir.mkdir(parents=True, exist_ok=True)

        for item in prompts:
            img_id = item["id"]
            prompt = item["description"]

            logger.info(f"Generating image {img_id}")

            image = self.pipe(
                prompt=prompt,
                num_inference_steps=25,
                guidance_scale=7.5
            ).images[0]

            out_path = output_dir / f"bg_{img_id:03d}.png"
            image.save(out_path)

        logger.info("Image generation complete")

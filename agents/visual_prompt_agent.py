import json
from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent
from config.settings import settings
from openai import OpenAI


class VisualPromptAgent(BaseAgent):
    def __init__(self):
        super().__init__("VisualPromptAgent")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_path = Path("prompts/visual_prompt.txt")

    def load_prompt(self, variables: dict) -> str:
        template = self.prompt_path.read_text()
        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def run(self, episode_number: int, metadata: dict, script: str) -> dict:
        logger.info(f"Generating visual prompts for episode {episode_number}")

        prompt = self.load_prompt({
            "title": metadata["title"],
            "genre": metadata["genre"],
            "tone": metadata["tone"],
            "episode_number": episode_number,
            "script": script[:12000]  # token safety
        })

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate cinematic visual prompts."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1500
        )

        raw = response.choices[0].message.content.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.error("Failed to parse visual prompt JSON")
            raise

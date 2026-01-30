import json
from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent
from config.settings import settings

from openai import OpenAI


class StoryArchitectAgent(BaseAgent):
    def __init__(self):
        super().__init__("StoryArchitect")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_path = Path("prompts/story_architect.txt")

    def load_prompt(self, variables: dict) -> str:
        template = self.prompt_path.read_text()
        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def run(
        self,
        genre: str,
        theme: str,
        episode_count: int = 4,
        audience: str = "general"
    ) -> dict:

        logger.info("Generating story blueprint")
        prompt = self.load_prompt({
            "genre": genre,
            "theme": theme,
            "episode_count": episode_count,
            "audience": audience,
        })

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a structured output generator."},
                {"role": "user", "content": prompt},
            ],
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

        content = response.choices[0].message.content.strip()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON returned by model")
            raise e

        self.validate(data)
        return data

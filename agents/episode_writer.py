from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent
from config.settings import settings
from openai import OpenAI


class EpisodeWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("EpisodeWriter")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_path = Path("prompts/episode_writer.txt")

    def load_prompt(self, variables: dict) -> str:
        template = self.prompt_path.read_text()
        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

    def run(self, story_meta: dict, episode: dict) -> str:
        logger.info(f"Writing episode {episode['episode']}: {episode['title']}")

        prompt = self.load_prompt({
            "story_title": story_meta["title"],
            "genre": story_meta["genre"],
            "theme": story_meta["theme"],
            "tone": story_meta["tone"],
            "episode_number": episode["episode"],
            "episode_title": episode["title"],
            "episode_summary": episode["summary"],
        })

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write long-form narration prose."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=2200,
        )

        script = response.choices[0].message.content.strip()
        self.validate(script)
        return script

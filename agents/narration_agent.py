import subprocess
from pathlib import Path
from loguru import logger
from agents.base_agent import BaseAgent


class NarrationAgent(BaseAgent):
    def __init__(self):
        super().__init__("NarrationAgent")

        self.voice_path = Path("assets/voices/en_US-lessac-medium.onnx")
        if not self.voice_path.exists():
            raise FileNotFoundError(f"Voice model not found: {self.voice_path}")

    # -----------------------------
    # EMOTION LAYER (CRITICAL)
    # -----------------------------
    def add_emotional_structure(self, text: str) -> str:
        """
        Inject pauses, breathing space, and dramatic pacing
        to make narration feel emotional instead of monotone.
        """
        text = text.replace("\n", " ")

        text = text.replace(". ", ".\n\n")
        text = text.replace("? ", "?\n\n")
        text = text.replace("! ", "!\n\n")
        text = text.replace("...", "...\n\n")
        text = text.replace("—", " — ")

        # Slow down emotional phrases
        text = text.replace("She knew", "She knew...\n\n")
        text = text.replace("He realized", "He realized...\n\n")
        text = text.replace("But then", "But then...\n\n")

        return text.strip()

    # -----------------------------
    # SAFE CHUNKING
    # -----------------------------
    def chunk_text(self, text: str, max_chars: int = 400) -> list[str]:
        chunks = []
        current = ""

        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            if len(current) + len(paragraph) <= max_chars:
                current += paragraph + "\n\n"
            else:
                chunks.append(current.strip())
                current = paragraph + "\n\n"

        if current.strip():
            chunks.append(current.strip())

        logger.info(f"Script split into {len(chunks)} emotional chunks")
        return chunks

    # -----------------------------
    # MAIN EXECUTION
    # -----------------------------
    def run(self, script_path: Path, output_path: Path):
        logger.info(f"Generating emotional narration for {script_path.name}")

        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        raw_text = script_path.read_text(encoding="utf-8")

        emotion_text = self.add_emotional_structure(raw_text)
        chunks = self.chunk_text(emotion_text)

        temp_dir = output_path.parent / "temp_audio"
        temp_dir.mkdir(parents=True, exist_ok=True)

        wav_files = []

        for i, chunk in enumerate(chunks):
            temp_wav = temp_dir / f"chunk_{i:03d}.wav"

            logger.debug(f"Generating chunk {i + 1}/{len(chunks)}")

            process = subprocess.run(
                [
                    "piper",
                    "--model", str(self.voice_path),
                    "--output_file", str(temp_wav)
                ],
                input=chunk,
                text=True,
                capture_output=True
            )

            if process.returncode != 0:
                logger.error(f"Piper failed on chunk {i}")
                logger.error(process.stderr)
                raise RuntimeError("Piper TTS failed")

            if not temp_wav.exists() or temp_wav.stat().st_size == 0:
                raise RuntimeError(f"Invalid audio chunk: {temp_wav}")

            wav_files.append(temp_wav)

        self.merge_audio(wav_files, output_path)
        logger.info(f"Final emotional narration saved to {output_path}")

    # -----------------------------
    # AUDIO MERGE
    # -----------------------------
    def merge_audio(self, wav_files: list[Path], output_path: Path):
        concat_file = output_path.parent / "concat.txt"
        concat_file.write_text(
            "\n".join([f"file '{wav.absolute()}'" for wav in wav_files]),
            encoding="utf-8"
        )

        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-c", "copy",
                str(output_path)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            logger.error("FFmpeg merge failed")
            logger.error(result.stderr)
            raise RuntimeError("Audio merge failed")

        if not output_path.exists() or output_path.stat().st_size == 0:
            raise RuntimeError("Final narration file is invalid")

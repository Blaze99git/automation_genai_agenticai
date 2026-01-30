import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.base_agent import BaseAgent

class DummyAgent(BaseAgent):
    def run(self):
        return "Hello from agent"

def main():
    agent = DummyAgent("TestAgent")
    print(agent.run())

if __name__ == "__main__":
    main()

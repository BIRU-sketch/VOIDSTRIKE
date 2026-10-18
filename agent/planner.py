from core.gemini_client import GeminiClient

class Planner:
    def __init__(self, gemini=None):
        self.gemini = gemini or GeminiClient()

    def create_plan(self, task: str) -> list[str]:
        prompt = (
            f"break this task into simple, sequential steps (1 per line):\n"
            f"task: {task}\n"
            f"return only the steps, no extra explanation."
        )
        return self._get_steps(prompt, fallback=[task])

    def replan(self, task: str, failed_plan: list[str], error: str) -> list[str]:
        plan_text = "\n".join(f"- {s}" for s in failed_plan) if isinstance(failed_plan, list) else str(failed_plan)
        prompt = (
            f"the previous plan failed. create a revised sequential plan to achieve the goal.\n"
            f"goal: {task}\n"
            f"failed Plan:\n{plan_text}\n"
            f"error Encountered: {error}\n"
            f"return only the revised steps (1 per line), no extra explanation."
        )
        return self._get_steps(prompt, fallback=failed_plan if isinstance(failed_plan, list) else [task])

    def _get_steps(self, prompt: str, fallback: list[str]) -> list[str]:
        reply = self.gemini.send(prompt)
        if "something went wrong:" in reply:
            return fallback

        steps = [
            line.strip().lstrip("-*0123456789. ")
            for line in reply.splitlines()
            if line.strip()
        ]
        return steps if steps else fallback

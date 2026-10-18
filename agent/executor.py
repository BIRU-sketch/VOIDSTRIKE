import platform
import re
from agent.planner import Planner
from agent.shell_runner import ShellRunner
from core.gemini_client import GeminiClient

ROUTER_SYSTEM="You classify messages. Answer with exactly one word."
ROUTER_PROMPT=("Is this message a request to DO something on the computer (run commands, "
    "create/move/read files, install things, open apps, system tasks) or just "
    "conversation/question?\nAnswer TASK or CHAT.\n\nMessage: {text}")
STEP_SYSTEM =(f"You are an automation agent on {platform.system()}. You complete ONE step at a time using the "
    "run_shell tool. Run the needed command(s), read the output, and confirm the step "
    "really worked. If something is already done, treat it as success. "
    "Never invent output. End your reply with exactly one line:\n"
    "STEP_OK: <short result>\nor\nSTEP_FAILED: <reason>")
class Executor:
    MAX_REPLANS=2
    def __init__(self, chat_client:GeminiClient,on_progress=None, shell: ShellRunner=None):
        self.chat = chat_client
        self.worker= GeminiClient()
        self.planner=Planner(self.worker)
        self.shell = shell or ShellRunner(timeout=30)
        self.on_progress = on_progress or (lambda s:None)
    def handle(self, text:str):
        if not self._is_task(text):
            return self.chat.send(text)
        return self._run_task(text)
    def _is_task(self, text):
        reply =self.worker.generate(ROUTER_PROMPT.format(text=text),system=ROUTER_SYSTEM)
        return reply.strip().upper().startswith("TASK")
    def _run_shell(self, command:str):
        self.on_progress(f"  $ {command}")
        result = self.shell.run(command)
        if result.startswith("BLOCKED"):
            self.on_progress(f"  x {result}")
        return result
    def _run_task(self, task:str):
        self.worker.reset()
        plan = self.planner.create_plan(task)
        replans =0
        while True:
            self.on_progress("Plan:\n" + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(plan)))
            results, failed = [], None

            for i, step in enumerate(plan):
                self.on_progress(f"Step {i+1}/{len(plan)}: {step}")
                ok, out = self._run_step(task, plan, i, results)
                if ok:
                    results.append((step, out))
                    self.on_progress(f"  ^{out}")
                else:
                    failed=(step, out)
                    self.on_progress(f"  x{out}")
                    break
            if failed is None:
                return self._summarize(task, results)
            if replans >=self.MAX_REPLANS:
                return "Couldn't finish this"
            replans+=1
            self.on_progress(f" Replanning.. {replans}/{self.MAX_REPLANS}")
            self.worker.reset()
            plan=self.planner.replan(task, plan, f"{failed[0] }-> {failed[1]}")
    def _run_step(self, task, plan, idx,results):
        numbered = "\n".join(f"{i+1}. {s}" for i, s in enumerate(plan))
        done = "\n".join(f"- {s}: {r}" for s, r in results) or "(none yet)"
        prompt = (
            f"Overall task: {task}\n\nFull plan:\n{numbered}\n\n"
            f"Completed so far:\n{done}\n\n"
            f"Current step ({idx+1}/{len(plan)}): {plan[idx]}\n"
            f"Working directory: {self.shell.base_dir}"
        )
        reply = self.worker.run_with_tools(
            prompt, [self._run_shell], system=STEP_SYSTEM.format(os=platform.system())
        )
        if reply.startswith("something went wrong"):
            return False, reply
        m = re.search(r"STEP_(OK|FAILED):\s*(.*)", reply, re.S)
        if not m:
            return True, reply.strip()[:300]
        return m.group(1) == "OK", m.group(2).strip()[:300]
    def _summarize(self, task, results):
        steps = "\n".join(f"- {s}: {r}" for s, r in results)
        reply = self.worker.generate(
            f"Task: {task}\n\nCompleted steps:\n{steps}\n\n"
            "Write a short, friendly summary of what was done and the outcome.",
            system="You summarize completed computer tasks briefly.",
        )
        return steps if reply.startswith("something went wrong") else reply
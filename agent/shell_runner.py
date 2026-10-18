import os 
import re
import subprocess
from pathlib import Path

class ShellRunner:
    BLOCKED_PATTERNS = [
        r"\brm\s+-[a-z]*[rf]",
        r"\b(sudo|su)\b",
        r"\b(shutdown|reboot|poweroff|halt|init)\b",
        r"\b(mkfs|dd|fdisk|parted)\b",
        r":\(\)\s*\{.*\}",
        r"(/etc/passwd|/etc/shadow|\.ssh/|\.aws/|\.env\b)",
        r"\b(curl|wget)\b.*\|\s*(ba|z)?sh",
        r"\bformat\s+[a-z]:",
        r"\b(del|rmdir|rd)\s+/[sq]",
        r"\bchmod\s+-R\s+777\b",
    ]
    def __init__(self, timeout: int =30, base_dir: str=None, max_output_chars: int=1000):
        self.timeout=timeout
        self.max_output_chars=max_output_chars
        self.base_dir = Path(base_dir).expanduser().resolve() if base_dir else Path.cwd()
    def _is_safe(self, command:str):
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"unsafe pattern blocked: {pattern}"
        return True, ""
    def _truncate(self, text:str):
        if len(text)<= self.max_output_chars:
            return text
        return text[:self.max_output_chars]+f"\n truncated,{len(text)} total"
    def _clean_env(self):
        return os.environ.copy()
    def run(self, command:str):
        command = command.strip()
        if not command:
            return "error: empty command"
        safe, reason=self._is_safe(command)
        if not safe:
            return f"BLOCKED: {reason}"
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                encoding="utf-8",
                text=True,
                errors="replace",
                timeout=self.timeout,
                cwd= str(self.base_dir),
                env = self._clean_env()
            )
        except subprocess.TimeoutExpired:
            return f"error: timed out after {self.timeout}s"
        except Exception as e:
            return f"error: {str(e)}"
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode ==0:
            out=stdout
            if stderr:
                out+=f"\n[stderr]\n {stderr}"
            return self._truncate(out.strip()) or "success (no output)"
        return self._truncate(f"error (code {result.returncode}): {stderr or stdout}")

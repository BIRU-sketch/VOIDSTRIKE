import threading

import customtkinter as ctk
from agent.executor import Executor
import config
from core.gemini_client import GeminiClient
from ui import theme
from ui.header import Header
from ui.chat_view import ChatView
from ui.input_bar import InputBar

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title(f"{config.name} — AI Assistant")
        self.geometry(config.window_size)
        self.minsize(*config.min_window_size)
        self.configure(fg_color=theme.BG)

        self.gemini = GeminiClient()
        self.executor =Executor(self.gemini, on_progress=self._on_progress)
        self.progress_lines=[]
        self.busy = False
        self.thinking_bubble = None

        self.header = Header(self, on_clear=self.clear_chat, on_exit=self.destroy)
        self.header.pack(fill="x")

        self.chat = ChatView(self)
        self.chat.pack(fill="both", expand=True, padx=8, pady=(6, 0))

        self.input_bar = InputBar(self, on_send=self.handle_send)
        self.input_bar.pack(fill="x", padx=12, pady=12)

        # Welcoming message
        self.chat.add_message(f"Hello! I'm {config.name}. How can I help you today?", "bot")
        self.input_bar.entry.focus()


    def handle_send(self, text):
        if self.busy:
            return
        self.chat.add_message(text, "user")
        self.busy = True
        self.input_bar.set_enabled(False)
        self.header.set_status("Thinking...", theme.ACCENT)
        self.thinking_bubble = self.chat.add_message("Thinking...", "bot")
        self.progress_lines=[]
        threading.Thread(target=self._ask, args=(text,), daemon=True).start()

    def _ask(self, text):
        reply = self.executor.handle(text)
        self.after(0, self._show_reply, reply)
    def _on_progress(self, line):
        self.after(0, self._show_progress,line)
    def _show_progress(self , line):
        self.progress_lines.append(line)
        if self.thinking_bubble is not None:
            self.thinking_bubble.set_text("\n".join(self.progress_lines[-12:]))
        self.header.set_status(line.strip()[:40], theme.ACCENT)
        self.chat._scroll_to_bottom()
    def _show_reply(self, reply):
        if self.thinking_bubble is not None:
            if self.progress_lines:
                self.thinking_bubble.set_text("\n".join(self.progress_lines))
                self.chat.add_message(reply, "bot")
            else:
                self.thinking_bubble.set_text(reply)
            self.thinking_bubble = None
        self.busy = False
        self.input_bar.set_enabled(True)
        self.header.set_status("Online", theme.ONLINE)
        self.chat._scroll_to_bottom()

    def clear_chat(self):
        if self.busy:
            return
        self.chat.clear()
        self.gemini.reset()
        self.chat.add_message("Chat cleared. What's next?", "bot")

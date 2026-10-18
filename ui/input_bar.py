import customtkinter as ctk
from ui import theme

class InputBar(ctk.CTkFrame):
    def __init__(self, parent, on_send):
        super().__init__(
            parent,
            fg_color=theme.PANEL,
            corner_radius=22,
            border_width=1,
            border_color=theme.BORDER,
        )
        self.on_send = on_send

        self.entry = ctk.CTkTextbox(
            self,
            height=40,
            fg_color="transparent",
            text_color=theme.TEXT,
            font=theme.FONT_BODY,
            wrap="word",
            border_width=0,
            activate_scrollbars=False,
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(14, 6), pady=4)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<KeyRelease>", self._on_key_release)

        # Subtle floating placeholder
        self.placeholder_lbl = ctk.CTkLabel(
            self.entry,
            text="Ask anything...",
            font=theme.FONT_BODY,
            text_color=theme.MUTED,
            fg_color="transparent",
        )
        self.placeholder_lbl.place(x=8, y=6)
        self.placeholder_lbl.bind("<Button-1>", lambda e: self.entry.focus())

        self.send_btn = ctk.CTkButton(
            self,
            text="↑",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=theme.USER_BUBBLE,
            hover_color=theme.USER_BUBBLE_HOVER,
            font=theme.FONT_SEND,
            command=self._submit,
        )
        self.send_btn.pack(side="right", padx=(0, 6), pady=4)

    def _on_key_release(self, event=None):
        if self.entry.get("1.0", "end-1c").strip():
            self.placeholder_lbl.place_forget()
        else:
            self.placeholder_lbl.place(x=8, y=6)

    def _on_enter(self, event):
        if event.state & 0x1:  # shift held -> new line
            return None
        self._submit()
        return "break"

    def _submit(self):
        text = self.entry.get("1.0", "end").strip()
        if not text:
            return
        self.entry.delete("1.0", "end")
        self.placeholder_lbl.place(x=8, y=6)
        self.on_send(text)

    def set_enabled(self, enabled):
        self.send_btn.configure(state="normal" if enabled else "disabled")
        if enabled:
            self.entry.focus()
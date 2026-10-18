import customtkinter as ctk
from ui import theme

class MessageBubble(ctk.CTkFrame):
    def __init__(self, parent, text, sender="bot"):
        super().__init__(parent, fg_color="transparent")
        is_user = sender == "user"
        self.label = ctk.CTkLabel(
            self,
            text=text,
            wraplength=theme.BUBBLE_WRAP,
            justify="left",
            font=theme.FONT_BODY,
            text_color="#ffffff" if is_user else theme.TEXT,
            fg_color=theme.USER_BUBBLE if is_user else theme.BOT_BUBBLE,
            border_width=0 if is_user else 1,
            border_color=theme.BOT_BORDER,
            corner_radius=theme.BUBBLE_RADIUS,
            padx=14,
            pady=9,
        )
        self.label.pack(
            side="right" if is_user else "left",
            padx=(48, 4) if is_user else (4, 48),
        )

    def set_text(self, text):
        self.label.configure(text=text)

    def send_text(self, text):
        self.set_text(text)
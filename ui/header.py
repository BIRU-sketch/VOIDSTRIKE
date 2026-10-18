import customtkinter as ctk
import config
from ui import theme
from ui.orb import Orb

class Header(ctk.CTkFrame):
    def __init__(self, parent, on_clear, on_exit):
        super().__init__(
            parent,
            fg_color=theme.PANEL,
            corner_radius=0,
            height=66,
            border_width=1,
            border_color=theme.BORDER,
        )
        self.pack_propagate(False)

        # Ambient AI Orb Avatar
        self.orb = Orb(self, size=38, bg=theme.PANEL)
        self.orb.pack(side="left", padx=(16, 10), pady=14)

        # Titles & Status
        titles = ctk.CTkFrame(self, fg_color="transparent")
        titles.pack(side="left", fill="y", pady=12)

        ctk.CTkLabel(
            titles,
            text=config.name,
            font=theme.FONT_TITLE,
            text_color=theme.TEXT,
        ).pack(anchor="w")

        self.status = ctk.CTkLabel(
            titles,
            text="online",
            font=theme.FONT_SMALL,
            text_color=theme.ONLINE,
        )
        self.status.pack(anchor="w")

        # Action Buttons
        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(side="right", padx=(0, 16))

        ctk.CTkButton(
            btn_box,
            text="Exit",
            width=54,
            height=28,
            corner_radius=14,
            fg_color=theme.BTN_DANGER,
            hover_color=theme.BTN_DANGER_HOVER,
            text_color=theme.TEXT,
            font=theme.FONT_SMALL,
            command=on_exit,
        ).pack(side="right", padx=(6, 0))

        ctk.CTkButton(
            btn_box,
            text="Clear",
            width=54,
            height=28,
            corner_radius=14,
            fg_color=theme.BTN_NEUTRAL,
            hover_color=theme.BTN_NEUTRAL_HOVER,
            text_color=theme.TEXT,
            font=theme.FONT_SMALL,
            command=on_clear,
        ).pack(side="right")

    def set_status(self, text, color):
        display_text = text if text.startswith("●") else f"● {text.capitalize()}"
        self.status.configure(text=display_text, text_color=color)
        if "think" in text.lower():
            self.orb.set_state("thinking")
        else:
            self.orb.set_state("idle")
        
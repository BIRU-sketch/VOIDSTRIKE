import customtkinter as ctk 
from ui import theme
from ui.message_bubble import MessageBubble

class ChatView(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=theme.BG,
            corner_radius=0,
            scrollbar_button_color=theme.BTN_NEUTRAL,
            scrollbar_button_hover_color=theme.BTN_NEUTRAL_HOVER,
        )

    def add_message(self, text, sender="bot"):
        bubble = MessageBubble(self, text, sender)
        bubble.pack(fill="x", pady=5, padx=8)
        self._scroll_to_bottom()
        return bubble

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _scroll_to_bottom(self):
        self.after(60, lambda: self._parent_canvas.yview_moveto(1.0))
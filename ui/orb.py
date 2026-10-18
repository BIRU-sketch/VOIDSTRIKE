import math
import tkinter as tk

from ui import theme

def _rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (1,3,5))

def _blend(c1,c2,t):
    a, b = _rgb(c1), _rgb(c2)
    r, g, bl = (int(a[i]+(b[i]-a[i])*t) for i in range(3))
    return f"#{r:02x}{g:02x}{bl:02x}"
class Orb(tk.Canvas):
    def __init__(self, parent, size=170, bg=theme.BG):
        super().__init__(parent, width=size, height=size, bg=bg, highlightthickness=0)
        self.size=size
        self.bg_color=bg
        self.state="idle"
        self.t=0.0
        self._animate()
    def set_state(self, state):
        self.state=state
    def _animate(self):
        try:
            self.delete("all")
        except tk.TclError:
            return
        thinking =self.state == "thinking"
        self.t += 0.14 if thinking else 0.05
        pulse = (math.sin(self.t)+1)/2

        c = self.size /2
        core = self.size  * 0.2 +pulse *self.size*(0.05 if thinking else 0.03)
        tint = _blend(theme.ACCENT, theme.ACCENT2, pulse)
        layers =12
        for i in range (layers, 0, -1):
            r = core +i*self.size*0.017
            strength = (1-i/layers)**2 * (0.45+0.4*pulse)
            color = _blend(self.bg_color, tint, strength)
            self.create_oval(c-r,c-r,c+r,c+r,fill=color, outline="")
        self.create_oval(
            c-core, c-core, c+core,c+core,
            fill=_blend(tint,"#ffffff", 0.25), outline="",
        )
        h= core * 0.5
        self.create_oval(
            c-h,c-h*1.2, c+h *0.4, c-h *0.1,
            fill=_blend(tint,"#ffffff", 0.7), outline="",
        )
        if thinking:
            r = core + self.size * 0.07
            self.create_arc(
                c-r, c-r, c+r, c+r,
                start =-(self.t *220)%360 , extent=110,
                style ="arc", outline = "#ffffff", width= 3,
            )
        self.after(33, self._animate)
import tkinter as tk

class ToolTip:
    def __init__(self, widget: tk.Widget, text: str, bg: str, fg: str, font: tuple):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.button_1_press_count = 0
        widget.bind("<Button-1>", self.show)
        self.bg = bg
        self.fg = fg
        self.font = font

    def show(self, event=None):
        if self.button_1_press_count % 2 == 1:
            self.hide()
            return

        def follow(event=None):
            if self.tooltip_window:
                x = self.widget.winfo_rootx() 
                y = self.widget.winfo_rooty() + self.widget.winfo_height()
                self.tooltip_window.wm_geometry("+%d+%d" % (x, y))


        self.button_1_press_count += 1
        
        # Get widget position
        x = self.widget.winfo_rootx() 
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        
        # Create tooltip window
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Remove window decorations
        self.tooltip_window.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, background=self.bg,
                         relief="solid", borderwidth=1, fg=self.fg,
                         font=self.font)
        label.pack(ipadx=1)

        self.widget.winfo_toplevel().bind("<Configure>", follow)


    def hide(self, event=None):
        if self.tooltip_window:
            self.button_1_press_count = 0
            self.tooltip_window.destroy()
            self.tooltip_window = None

# Example usage:
if __name__ == "__main__":

    root = tk.Tk()
    button = tk.Button(root, text="Hover over me")
    button.pack(padx=50, pady=50)

    tooltip = ToolTip(button, "This is a tooltip", "gray", "white", ("Arial", 10))

    root.mainloop()

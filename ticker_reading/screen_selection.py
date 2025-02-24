import tkinter as tk

class ScreenSelector:
    def __init__(self, master: tk.Tk):
        self.root = tk.Toplevel(master)
        self.root.attributes('-fullscreen', True)  # Make window fullscreen
        self.root.attributes('-topmost', True)     # Keep the window on top
        self.root.attributes('-alpha', 0.3)       # Make it transparent
        self.root.config(bg="black")              # Background overlay color

        # Create a Canvas to draw on
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Variables for tracking the rectangle
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selection = None

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.start_selection)  # Start rectangle
        self.canvas.bind("<B1-Motion>", self.update_selection)    # Update rectangle
        self.canvas.bind("<ButtonRelease-1>", self.end_selection) # Finalize selection

        # Optionally bind Escape to close without selecting
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def start_selection(self, event):
        """Start drawing the rectangle."""
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2, fill="white", stipple="gray12"
        )

    def update_selection(self, event):
        """Update the rectangle as the mouse moves."""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def end_selection(self, event):
        """Finalize the selection."""
        # Print the selection coordinates
        print(f"Selected area: Start=({self.start_x}, {self.start_y}), End=({event.x}, {event.y})")
        # Optionally destroy the window after selection
        self.root.destroy()

        x = self.start_x
        y = self.start_y
        width = event.x - x
        height = event.y - y

        self.selection = (x, y, width, height)
        self.root.quit()


    def run(self):
        self.root.mainloop()
        self.root.destroy()
        return self.selection



# Run the selector
if __name__ == "__main__":
    selector = ScreenSelector()
    selector.run()


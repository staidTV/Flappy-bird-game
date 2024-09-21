# pillars.py
import tkinter as tk
from random import randint

class Pillars:
    def __init__(self, canvas, x_position):
        self.canvas = canvas
        self.pipe_gap = 150
        self.pipe_width = 60
        self.gap_start = randint(100, 400)

        # Create top and bottom pipes
        self.top_pipe = self.canvas.create_rectangle(x_position, 0, x_position + self.pipe_width, self.gap_start, fill="blue")
        self.bottom_pipe = self.canvas.create_rectangle(x_position, self.gap_start + self.pipe_gap, x_position + self.pipe_width, 600, fill="blue")

    def move(self):
        """Move the pipes to the left."""
        self.canvas.move(self.top_pipe, -5, 0)
        self.canvas.move(self.bottom_pipe, -5, 0)

    def get_coords(self):
        """Return the coordinates of the pipes."""
        return self.canvas.bbox(self.top_pipe), self.canvas.bbox(self.bottom_pipe)

    def is_off_screen(self):
        """Check if the pipes are off the screen."""
        return self.canvas.coords(self.top_pipe)[2] < 0

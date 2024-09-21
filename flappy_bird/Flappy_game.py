# flappy_game.py
import tkinter as tk
from pillars import Pillars
from background import set_background

class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=400, height=600)
        self.canvas.pack()

        set_background(self.canvas)  # Set background to green

        self.bird = self.canvas.create_oval(50, 250, 90, 290, fill='yellow')
        self.gravity = 3
        self.bird_speed = 0
        self.is_game_over = False
        self.pillars = []

        # Key bindings for bird movement
        self.root.bind("<space>", self.flap)

        # Create initial pillars
        self.create_pillars()

        # Start the game loop
        self.update_game()

    def create_pillars(self):
        """Create new pillars at the right edge of the canvas."""
        new_pillar = Pillars(self.canvas, 400)
        self.pillars.append(new_pillar)

    def flap(self, event):
        """Make the bird flap upward."""
        self.bird_speed = -10

    def update_game(self):
        if not self.is_game_over:
            # Update bird position
            self.bird_speed += self.gravity
            self.canvas.move(self.bird, 0, self.bird_speed)

            # Get the bird's coordinates
            bird_coords = self.canvas.coords(self.bird)
            if bird_coords[1] <= 0 or bird_coords[3] >= 600:
                self.game_over()

            # Move and manage pillars
            self.move_pillars()
            self.check_collision()

            # Generate new pillars
            if len(self.pillars) > 0:
                pillar_coords = self.pillars[-1].get_coords()
                if pillar_coords[0][2] < 300:
                    self.create_pillars()

            # Continue game loop
            self.root.after(30, self.update_game)

    def move_pillars(self):
        """Move the pillars across the screen and remove off-screen pillars."""
        for pillar in self.pillars:
            pillar.move()

        # Remove pillars that are off-screen
        self.pillars = [pillar for pillar in self.pillars if not pillar.is_off_screen()]

    def check_collision(self):
        """Check for collisions between the bird and the pillars."""
        bird_coords = self.canvas.bbox(self.bird)
        for pillar in self.pillars:
            top_pipe_coords, bottom_pipe_coords = pillar.get_coords()

            # Check if bird hits top or bottom pipes
            if self.rect_overlap(bird_coords, top_pipe_coords) or self.rect_overlap(bird_coords, bottom_pipe_coords):
                self.game_over()

    def rect_overlap(self, rect1, rect2):
        """Check if two rectangles overlap."""
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[3] < rect2[1] or rect1[1] > rect2[3])

    def game_over(self):
        """Handle game over."""
        self.is_game_over = True
        self.canvas.create_text(200, 300, text="Game Over", font=('Helvetica', 24), fill='red')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flappy Bird")
    game = FlappyBirdGame(root)
    root.mainloop()

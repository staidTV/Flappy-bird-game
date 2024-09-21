import tkinter as tk
import random

# Constants
WIDTH = 400
HEIGHT = 600
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
BIRD_Y_VELOCITY = 0
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 5

# Colors
WHITE = "white"
BLACK = "black"
GREEN = "green"
BLUE = "sky blue"
BROWN = "brown"

class FlappyBird:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BLUE)
        self.canvas.pack()

        self.bird = self.canvas.create_rectangle(50, HEIGHT // 2, 50 + BIRD_WIDTH, HEIGHT // 2 + BIRD_HEIGHT, fill="yellow")
        self.ground = self.canvas.create_rectangle(0, HEIGHT - 100, WIDTH, HEIGHT, fill=BROWN)

        self.pipes = []
        self.pipe_timer = 0
        self.bird_velocity = BIRD_Y_VELOCITY
        self.bird_y = HEIGHT // 2

        self.setup_game()

    def setup_game(self):
        self.canvas.bind_all("<space>", self.flap)
        self.root.after(20, self.update)

    def flap(self, event):
        self.bird_velocity = FLAP_STRENGTH

    def update(self):
        self.bird_velocity += GRAVITY
        self.bird_y += self.bird_velocity
        self.canvas.move(self.bird, 0, self.bird_velocity)
        
        if self.canvas.coords(self.bird)[1] < 0 or self.canvas.coords(self.bird)[3] > HEIGHT - 100:
            self.game_over()
            return

        self.pipe_timer += 1
        if self.pipe_timer > 50:
            self.pipe_timer = 0
            self.create_pipe()

        self.move_pipes()
        self.check_collision()

        self.root.after(20, self.update)

    def create_pipe(self):
        height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        top_pipe = self.canvas.create_rectangle(WIDTH, 0, WIDTH + PIPE_WIDTH, height, fill=GREEN)
        bottom_pipe = self.canvas.create_rectangle(WIDTH, height + PIPE_GAP, WIDTH + PIPE_WIDTH, HEIGHT - 100, fill=GREEN)
        self.pipes.append((top_pipe, bottom_pipe))

    def move_pipes(self):
        for top_pipe, bottom_pipe in self.pipes:
            self.canvas.move(top_pipe, -PIPE_SPEED, 0)
            self.canvas.move(bottom_pipe, -PIPE_SPEED, 0)

        # Remove off-screen pipes
        for top_pipe, bottom_pipe in self.pipes:
            if self.canvas.coords(top_pipe)[2] < 0:
                self.canvas.delete(top_pipe)
                self.canvas.delete(bottom_pipe)
                self.pipes.remove((top_pipe, bottom_pipe))

    def check_collision(self):
        bird_coords = self.canvas.coords(self.bird)
        for top_pipe, bottom_pipe in self.pipes:
            top_coords = self.canvas.coords(top_pipe)
            bottom_coords = self.canvas.coords(bottom_pipe)

            if (bird_coords[2] > top_coords[0] and bird_coords[0] < top_coords[2] and
                (bird_coords[1] < top_coords[3] or bird_coords[3] > bottom_coords[1])):
                self.game_over()
                return

    def game_over(self):
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill=BLACK, font=("Arial", 24))
        self.root.after_cancel(self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBird(root)
    root.mainloop()
 
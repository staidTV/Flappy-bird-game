import tkinter as tk
import random

# Game settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRAVITY = 2
JUMP_STRENGTH = -20
PIPE_SPEED = 5
PIPE_GAP = 150
PIPE_WIDTH = 80
PIPE_SPACING = 300
BIRD_SIZE = 30

# Bird class
class Bird:
    def __init__(self, canvas):
        self.canvas = canvas
        self.bird = canvas.create_rectangle(50, WINDOW_HEIGHT // 2 - BIRD_SIZE // 2, 
                                            50 + BIRD_SIZE, WINDOW_HEIGHT // 2 + BIRD_SIZE // 2, 
                                            fill='yellow')
        self.y_velocity = 0
    
    def jump(self):
        self.y_velocity = JUMP_STRENGTH
    
    def move(self):
        self.y_velocity += GRAVITY
        self.canvas.move(self.bird, 0, self.y_velocity)
        
        # Get bird's position
        bird_coords = self.canvas.coords(self.bird)
        
        # Prevent bird from going out of the window (top and bottom)
        if bird_coords[1] < 0:
            self.canvas.move(self.bird, 0, -bird_coords[1])
            self.y_velocity = 0
        if bird_coords[3] > WINDOW_HEIGHT:
            self.canvas.move(self.bird, 0, WINDOW_HEIGHT - bird_coords[3])
            self.y_velocity = 0

    def get_position(self):
        return self.canvas.coords(self.bird)

# Pipe class
class Pipe:
    def __init__(self, canvas, x):
        self.canvas = canvas
        self.top_pipe = None
        self.bottom_pipe = None
        self.passed = False  # Track if the bird has passed this pipe
        self.create_pipes(x)
    
    def create_pipes(self, x):
        gap_start = random.randint(100, WINDOW_HEIGHT - 100 - PIPE_GAP)
        self.top_pipe = self.canvas.create_rectangle(x, 0, x + PIPE_WIDTH, gap_start, fill='green')
        self.bottom_pipe = self.canvas.create_rectangle(x, gap_start + PIPE_GAP, x + PIPE_WIDTH, WINDOW_HEIGHT, fill='green')
    
    def move(self):
        self.canvas.move(self.top_pipe, -PIPE_SPEED, 0)
        self.canvas.move(self.bottom_pipe, -PIPE_SPEED, 0)
    
    def get_position(self):
        return self.canvas.coords(self.top_pipe), self.canvas.coords(self.bottom_pipe)
    
    def off_screen(self):
        top_coords = self.canvas.coords(self.top_pipe)
        return top_coords[2] < 0

# Game class
class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='skyblue')
        self.canvas.pack()
        
        self.bird = Bird(self.canvas)
        self.pipes = []
        self.pipe_timer = 0
        
        self.is_game_over = False
        self.score = 0
        
        # Display the score
        self.score_text = self.canvas.create_text(WINDOW_WIDTH // 2, 50, text=f"Score: {self.score}", font=('Arial', 24), fill='white')

        # Bind the spacebar key to bird jump
        self.root.bind('<space>', self.jump)
        
        # Start game loop
        self.update_game()

    def jump(self, event):
        if not self.is_game_over:
            self.bird.jump()

    def check_collision(self):
        bird_coords = self.bird.get_position()
        for pipe in self.pipes:
            top_coords, bottom_coords = pipe.get_position()
            
            # Check collision with top or bottom pipes
            if (bird_coords[2] > top_coords[0] and bird_coords[0] < top_coords[2]):
                if bird_coords[1] < top_coords[3] or bird_coords[3] > bottom_coords[1]:
                    self.is_game_over = True

    def update_score(self):
        bird_coords = self.bird.get_position()
        for pipe in self.pipes:
            pipe_coords = pipe.get_position()[0]
            # Check if bird has passed the pipe
            if not pipe.passed and pipe_coords[2] < bird_coords[0]:
                self.score += 1
                pipe.passed = True
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def update_game(self):
        if not self.is_game_over:
            # Move the bird
            self.bird.move()

            # Add new pipes
            if self.pipe_timer > PIPE_SPACING:
                self.pipes.append(Pipe(self.canvas, WINDOW_WIDTH))
                self.pipe_timer = 0
            self.pipe_timer += PIPE_SPEED

            # Move pipes, check for collisions, and update score
            for pipe in self.pipes:
                pipe.move()
            self.check_collision()
            self.update_score()

            # Remove off-screen pipes
            self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

        # Update the game loop every 50ms
        self.root.after(50, self.update_game)

# Create the game window
root = tk.Tk()
root.title("Flappy Bird Game")
game = FlappyBirdGame(root)
root.mainloop()

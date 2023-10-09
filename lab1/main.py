import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
PADDLE_HEIGHT = 10
BALL_SPEED = 7
PADDLE_SPEED = 10
GAME_DURATION = 5  # 5 seconds
PADDLE_WIDTH_CHANGE = 10  # Width change when pressing up/down arrow keys

class PingPongGame:
    PADDLE_WIDTH = 100  # Initial paddle width

    def __init__(self, window):
        self.window = window
        self.window.title("Ping Pong Game")

        self.instructions_label = tk.Label(self.window, text="Press Start to Begin\nUse Left and Right arrows to move the paddle\nUse Up and Down arrows to change paddle width", font=("Helvetica", 14))
        self.instructions_label.pack(side="top", pady=10)  # Place instructions label at the top

        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT - 60, bg="black")
        self.canvas.pack()

        self.restart_button = tk.Button(self.window, text="Restart", command=self.reset_game)
        self.restart_button.pack(side="left")

        self.start_button = tk.Button(self.window, text="Start", command=self.start_game)
        self.start_button.pack(side="left")

        self.score_label = tk.Label(self.window, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack(side="right")

        self.timer_label = tk.Label(self.window, text="", font=("Helvetica", 24))
        self.timer_label.pack()

        self.paddle_width_label = tk.Label(self.window, text=f"Paddle Width: {self.PADDLE_WIDTH}", font=("Helvetica", 12))
        self.paddle_width_label.pack(side="bottom")

        self.game_active = False  # Flag to control if the game is active
        self.score = 0
        self.remaining_time = GAME_DURATION
        self.paddle_movable = False  # Flag to control paddle movement
        self.collided_with_paddle = False  # Flag to track paddle collisions (initialize it to False)

        self.reset_game()

        # Bind key events
        self.window.bind("<KeyPress>", self.key_down)
        self.window.bind("<KeyRelease>", self.key_up)

        # Start the game loop
        self.update()

    def reset_game(self):
        self.canvas.delete("all")

        # Set the paddle width back to 100
        self.PADDLE_WIDTH = 100

        self.player_paddle = self.canvas.create_rectangle(WIDTH / 2 - self.PADDLE_WIDTH / 2, HEIGHT - 70,
                                                          WIDTH / 2 + self.PADDLE_WIDTH / 2,
                                                          HEIGHT - 70 - PADDLE_HEIGHT, fill="white")

        self.ball = self.canvas.create_oval(WIDTH / 2 - BALL_RADIUS, HEIGHT / 2 - BALL_RADIUS - 20,
                                            WIDTH / 2 + BALL_RADIUS, HEIGHT / 2 + BALL_RADIUS - 20, fill="white")

        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.player_paddle_speed = 0
        self.game_active = False
        self.restart_button.pack(side="left")  # Show the restart button
        self.start_button.pack(side="left")  # Show the start button
        self.score_label.config(text="Score: 0")
        self.score = 0
        self.timer_label.config(text="Press Start to Begin")
        self.paddle_movable = False  # Make the paddle immovable during countdown
        self.paddle_width_label.config(text=f"Paddle Width: {self.PADDLE_WIDTH}")

    def start_game(self):
        if not self.game_active:
            self.remaining_time = GAME_DURATION
            self.update_timer_label()
            self.game_active = True
            self.start_button.pack_forget()  # Hide the start button
            self.restart_button.pack()  # Show the restart button
            self.window.after(1000, self.countdown)  # Start the countdown
            self.paddle_movable = False  # Disallow paddle movement before countdown
            self.collided_with_paddle = False  # Track paddle collisions

    def countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_label()
            self.window.after(1000, self.countdown)  # Schedule the next update
        else:
            self.start_ball_movement()  # Start the ball movement when the countdown is finished
            self.paddle_movable = True  # Allow paddle movement after countdown

    def start_ball_movement(self):
        self.timer_label.config(text="")
        self.ball_speed_x = BALL_SPEED * random.choice((1, -1))
        self.ball_speed_y = -BALL_SPEED  # Ensure the ball always moves upward
        self.collided_with_paddle = False  # Reset collision flag

    def update_timer_label(self):
        self.timer_label.config(text=f"Time: {self.remaining_time}s")

    def update(self):
        if self.game_active:
            # Move the ball
            self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

            # Get ball coordinates
            ball_pos = self.canvas.coords(self.ball)

            # Collision with left and right walls
            if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
                self.ball_speed_x = -self.ball_speed_x

            # Collision with top wall
            if ball_pos[1] <= 0:
                self.ball_speed_y = -self.ball_speed_y
                self.collided_with_paddle = False  # Reset collision flag when ball hits top wall

            # Ball out of bounds (player loses)
            if ball_pos[3] >= HEIGHT - 60:
                self.end_game()

            # Collision with the player's paddle
            if (not self.collided_with_paddle and
                ball_pos[1] <= HEIGHT - 90 and ball_pos[3] >= HEIGHT - 80 and
                ball_pos[0] > self.canvas.coords(self.player_paddle)[0] and ball_pos[2] < self.canvas.coords(self.player_paddle)[2]):

                self.ball_speed_y = -BALL_SPEED
                self.increase_score()
                self.collided_with_paddle = True  # Set collision flag to True

            # Move the player's paddle if allowed
            if self.paddle_movable:
                # Ensure the paddle doesn't go beyond the left and right walls
                paddle_pos = self.canvas.coords(self.player_paddle)
                if (self.player_paddle_speed < 0 and paddle_pos[0] > 0) or (self.player_paddle_speed > 0 and paddle_pos[2] < WIDTH):
                    self.canvas.move(self.player_paddle, self.player_paddle_speed, 0)

        # Repeat the update function
        self.window.after(20, self.update)

    def increase_score(self):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

    def end_game(self):
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 20, text=f"Game Over! Score: {self.score}", fill="white", font=("Helvetica", 24))
        self.game_active = False
        self.restart_button.pack()  # Show the restart button
        self.paddle_movable = False  # Disallow paddle movement

    def key_down(self, event):
        key = event.keysym

        if self.paddle_movable:  # Only move paddle if allowed
            if key == "Left":
                self.player_paddle_speed = -PADDLE_SPEED
            elif key == "Right":
                self.player_paddle_speed = PADDLE_SPEED
            elif key == "Up":
                if self.PADDLE_WIDTH < WIDTH - PADDLE_WIDTH_CHANGE:
                    self.PADDLE_WIDTH += PADDLE_WIDTH_CHANGE  # Increase paddle width (if it's smaller than the maximum width)
                    self.update_paddle_visual()  # Update the visual representation
            elif key == "Down":
                if self.PADDLE_WIDTH > 50:
                    self.PADDLE_WIDTH -= PADDLE_WIDTH_CHANGE  # Decrease paddle width (if it's greater than the minimum width)
                    self.update_paddle_visual()  # Update the visual representation

    def key_up(self, event):
        key = event.keysym

        if key in ("Left", "Right"):
            self.player_paddle_speed = 0

    def update_paddle_visual(self):
        # Update the visual representation of the paddle
        paddle_pos = self.canvas.coords(self.player_paddle)
        self.canvas.coords(self.player_paddle, paddle_pos[0], paddle_pos[1], paddle_pos[0] + self.PADDLE_WIDTH, paddle_pos[3])
        self.paddle_width_label.config(text=f"Paddle Width: {self.PADDLE_WIDTH}")

if __name__ == "__main__":
    window = tk.Tk()
    game = PingPongGame(window)
    window.mainloop()
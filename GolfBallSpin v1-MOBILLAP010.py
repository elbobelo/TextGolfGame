import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

CIRCUMFERENCE = 0.134  # Corrected circumference of a golf ball
VERTICAL_VELOCITY = 5/7 * 34000 * math.sin(math.radians(14))

# Calculate the spin rate in RPM
spin_rate = (VERTICAL_VELOCITY / CIRCUMFERENCE) / 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the ball
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# Set up the red dot
dot_pos = ball_pos

angle = 0
prev_time = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate the spin rate decay per second
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - prev_time) / 1000  # Convert to seconds
    prev_time = current_time

    # Update the ball's position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Update the angle
    angle += spin_rate * elapsed_time * math.pi / 30  # Convert RPM to radians/sec

    # Calculate the spin rate decay per second
    spin_rate *= 0.999  # Added decay to slow down the spin rate**

    # Update the dot's position
    dot_pos = [ball_pos[0] + 45 * math.sin(angle),
               ball_pos[1] + 45 * math.cos(angle)]

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, ball_pos, 50)
    pygame.draw.circle(screen, RED, dot_pos, 5)
    pygame.display.flip()

    # Print the dot's position and spin rate
    print(f"Dot position: {dot_pos}")
    print(f"Spin rate: {spin_rate:.2f} RPM")

    # Cap the frame rate
    pygame.time.Clock().tick(60)
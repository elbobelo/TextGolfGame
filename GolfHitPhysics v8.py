import numpy as np
import pygame
import sys
import math

# Initialize Pygame
pygame.init()
# Create a display window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

test_names = [
    {'name': 'Velocity: ', 'start': 34, 'increment': 1},
    {'name': 'Angle: ', 'start': 14, 'increment': 2},
    {'name': 'Club Mass: ', 'start': 0.22, 'increment': .01},
    {'name': 'Lift: ', 'start': 0.4, 'increment': .01},
]
test = [d['start'] for d in test_names]
test_chosen = 0
def test_code():
    global test_chosen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_i, pygame.K_k):
                test_chosen = (
                        (test_chosen + (1 if event.key == pygame.K_k else -1)) % len(test))
            elif event.key in (pygame.K_j, pygame.K_l):
                test[test_chosen] += (
                    test_names[test_chosen]['increment'] if event.key == pygame.K_l
                    else -test_names[test_chosen]['increment'])
    list(map(lambda i: screen.blit(pygame.font.Font(
        None, 30 - (i - test_chosen) % len(test) * 5).render(test_names[i]['name'] + str(test[i]),
        True,
        (0xFF, 0x00, 0X00)),
        (10, 10 + (i - test_chosen) % len(test) * 20)), range(len(test))))

def run_simulation():
    global test_chosen

    class GolfBall:
        def __init__(self, mass=0.04593, radius=0.021335, ):
            self.mass = mass  # mass in kg
            self.radius = radius  # radius in meters

    # Create a golf ball object
    golf_ball = GolfBall()

    # Initial conditions
    velc = test[0]  # Impact velocity in m/s
    loftc = np.radians(test[1])  # Impact angle in degrees
    massc = test[2]  # Impact mass in kg

    pos = np.array([0.0, 0.0])  # Ball position
    # Calculate initial ball velocity
    vball = (velc * 1.67) / (1.0 + (golf_ball.mass / massc))
    vballi = ((np.cos(loftc)) ** 2 * (np.sin(np.pi / 2 - loftc)) * vball)
    vel = np.array([vballi * np.cos(loftc), vballi * np.sin(loftc)])  # Ball velocity in m/s

    # Time step
    dt = 0.1

    # Number of loops
    n_loops = 200

    # Lists to store position data
    x_positions = [0]
    y_positions = [0]

    clock = pygame.time.Clock()

    # Run the simulation
    while pos[1] >= 0 and 0 <= pos[0] <= screen_width and n_loops < 1000:

        speed = np.linalg.norm(vel)  # Magnitude of velocity vector
        rho = 1.225  # Air density at sea level (kg/m^3)
        eta = 1.8e-5  # Kinematic viscosity for air
        g = -9.8  # Gravity
        A = np.pi * golf_ball.radius ** 2  # Frontal area of the ball in m^2
        av = (2 * np.pi * test[0] * 60) / 360  # Convert RPM to angular velocity (rad/s)
        Re = rho * (golf_ball.radius * 2) * speed / eta  # Calculate Reynolds number
        Cd = np.interp(Re, np.linspace(6.5e4, 9e4, 100), np.linspace(0.5, 0.27, 100))
        # Calculate drag force
        Fd = 0.5 * rho * A * Cd * (speed ** 2) * vel / speed  # Include velocity normalization

        # Lift force (assuming constant upwards lift)
        lift_force = np.array([0, test[3]])  # Adjust lift force as needed

        CIRCUMFERENCE = 0.134  # Corrected circumference of a golf ball
        spin_rate = (velc / CIRCUMFERENCE) / 60

        # Calculate the lift force using the Magnus effect
        lift_force_magnus = 0.5 * rho * A * (spin_rate ** 2) * math.sin(loftc)

        # Calculate the spin rate decay per second
        spin_rate *= 0.999  # Added decay to slow down the spin rate**

        # Update the ball's acceleration after the spin rate decays
        acc = np.array([-Fd[0] / golf_ball.mass, g + lift_force[1] / golf_ball.mass + lift_force_magnus])
        # Update velocity
        vel += acc * dt

        # Update position
        pos = pos + vel * dt + 0.5 * acc * dt ** 2

        if pos[1] + golf_ball.radius >= screen_height:
            pos[1] = screen_height - golf_ball.radius
            vel = 0  # Simulate bouncing on ground

        # Append current position to lists
        x_positions.append(pos[0])
        y_positions.append(pos[1])

        n_loops += 1 # Increment number of loops
        screen.fill((0, 0, 0)) # Clear the display window
        test_code()  # TEST_CODE
        # Draw the ball
        pygame.draw.circle(screen, (255, 255, 255), (int(pos[0]*2), int(screen_height - pos[1]*2)),
                           int(golf_ball.radius * 100))  # Scale ball size for visibility

        # Update the display
        pygame.display.flip()

        # Set frame rate
        clock.tick(60)  # Adjust frame rate as needed

    # Print the maximum height and total x distance traveled
    max_height = max(y_positions)
    total_x_distance = sum(np.diff(x_positions))
    print(f"Maximum height: {max_height / 0.9144:.2f} yards")
    print(f"Total x distance traveled: {total_x_distance}")
    print(f"Total Distance: {total_x_distance / 0.9144:.2f} yards")


# Run the simulation 5 times
for _ in range(50000):
    # Clear the screen
    screen.fill((0, 0, 0))
    run_simulation()

# Quit Pygame
pygame.quit()
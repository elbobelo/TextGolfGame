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


def get_vel(club_vel, ball_mass, club_mass, club_loft):
    ball_vel = (club_vel * 1.67) / (1 + (ball_mass / club_mass))
    ball_veli = (np.cos(club_loft)) ** 2 * (np.sin(np.pi / 2 - club_loft)) * ball_vel
    vel = np.array([ball_veli * np.cos(club_loft), ball_veli * np.sin(club_loft)])
    return vel

def calculate_speed(vel):
    return np.linalg.norm(vel)


def get_reynolds_number(rho, golf_ball_radius, speed, eta):
    return rho * (golf_ball_radius * 2) * speed / eta


def get_drag_coefficient(Re):
    Cd_values = np.linspace(0.5, 0.27, 100)
    Re_values = np.linspace(6.5e4, 9e4, 100)
    return np.interp(Re, Re_values, Cd_values)


def get_drag_force(rho, A, Cd, speed, vel):
    Fd = 0.5 * rho * A * Cd * (speed ** 2) * vel / speed
    return Fd


def get_lift_force_magnus(spin_rate, circumference, rho, A, loftc):
    spin_rate_decay_per_second = (spin_rate / 60) * circumference
    lift_force_magnus = 0.5 * rho * A * (spin_rate_decay_per_second ** 2) * math.sin(loftc)
    return lift_force_magnus


def run_simulation():
    global test_chosen

    class GolfBall:
        def __init__(self, mass=0.04593, radius=0.021335, ):
            self.mass = mass  # mass in kg
            self.radius = radius  # radius in meters

    # Create a golf ball object
    golf_ball = GolfBall()

    # Initial club conditions
    velc = test[0]  # Impact velocity in m/s
    loftc = np.radians(test[1])  # Impact angle in degrees
    massc = test[2]  # Impact mass in kg

    pos = np.array([0.0, 0.0])  # Ball position
    # Calculate initial ball velocity
    vel = get_vel(velc, golf_ball.mass, massc, loftc) # Ball velocity in m/s

    circumference = 0.134
    vertical_velocity = 5 / 7 * 34000 * math.sin(loftc)
    spin_rate = (vertical_velocity / circumference) / 60

    # Time step
    dt = 0.1

    # Number of loops
    n_loops = 200

    # Lists to store position data
    x_positions = [0]
    y_positions = [0]

    clock = pygame.time.Clock()

    while pos[1] >= 0 and 0 <= pos[0] <= screen_width and n_loops < 1000:

        speed = calculate_speed(vel)

        rho = 1.225  # Air density at sea level (kg/m^3)
        eta = 1.8e-5  # Kinematic viscosity for air

        g = -9.8  # Gravity
        A = np.pi * golf_ball.radius ** 2  # Frontal area of the ball in m^2
        av = (2 * np.pi * test[0] * 60) / 360

        Re = get_reynolds_number(rho, golf_ball.radius, speed, eta)
        Cd = get_drag_coefficient(Re)

        Fd = get_drag_force(rho, A, Cd, speed, vel)

        lift_force = np.array([0, test[3]])

        lift_force_magnus = get_lift_force_magnus(spin_rate, circumference, rho, A, loftc)

        spin_rate *= 0.999  # Added decay to slow down the spin rate

        print(spin_rate)
        net_lift = lift_force[1] + lift_force_magnus
        acc = np.array([-Fd[0] / golf_ball.mass, g + net_lift / golf_ball.mass])
        #acc = np.array([-Fd[0] / golf_ball.mass, g + lift_force[1] / golf_ball.mass + lift_force_magnus])
        vel += acc * dt
        pos += vel * dt + 0.5 * acc * (dt ** 2)

        if pos[1] + golf_ball.radius >= screen_height:
            pos[1] = screen_height - golf_ball.radius
            vel = 0

        x_positions.append(pos[0])
        y_positions.append(pos[1])

        n_loops += 1
        screen.fill((0, 0, 0))
        test_code()# TEST_CODE
        # Draw the ball
        pygame.draw.circle(screen, (255, 255, 255), (int(pos[0] * 2), int(screen_height - pos[1] * 2)),
                           int(golf_ball.radius * 100))

        pygame.display.flip()
        clock.tick(60)

    # Print the maximum height and total x distance traveled
    max_height = max(y_positions)
    total_x_distance = sum(np.diff(x_positions))
    print(f"Maximum height: {max_height / 0.9144:.2f} yards")
    print(f"Total x distance traveled: {total_x_distance}")
    print(f"Total Distance: {total_x_distance / 0.9144:.2f} yards")


for _ in range(50000):
    screen.fill((0, 0, 0))
    run_simulation()

pygame.quit()
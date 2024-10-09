import numpy as np
import pygame
import sys
import math

# Constants
CLUB_VELOCITY = 34  # Impact velocity in m/s
CLUB_LOFT = np.radians(14)  # Impact angle in degrees
CLUB_MASS = 0.22  # Impact mass in kg
LIFT = 0.4
GOLF_BALL_MASS = 0.04593
GOLF_BALL_RADIUS = 0.021335
GOLF_BALL_A = np.pi * GOLF_BALL_RADIUS ** 2  # Frontal area of the ball in m^2
CIRCUMFERENCE = 0.134
VERTICAL_VELOCITY = 5 / 7 * 34000 * math.sin(CLUB_LOFT)
SPIN_RATE_DECAY_PER_SECOND = (VERTICAL_VELOCITY / CIRCUMFERENCE) / 60
AIR_DENSITY = 1.225  # Air density at sea level (kg/m^3)
KINEMATIC_VISCOSITY = 1.8e-5  # Kinematic viscosity for air
GRAVITY = -9.8


def get_vel(club_vel, club_mass, club_loft, ball_mass):
    transferred_energy_factor = (club_vel * 1.67) / (1 + (ball_mass / club_mass))
    post_impact_ball_speed = (np.cos(club_loft)) ** 2 * (np.sin(np.pi / 2 - club_loft)) * transferred_energy_factor
    vel = np.array([post_impact_ball_speed * np.cos(club_loft), post_impact_ball_speed * np.sin(club_loft)])
    return vel


def get_speed(vel):
    return np.linalg.norm(vel)


def get_reynolds_number(rho, radius, speed, viscosity):
    return rho * speed * (2 * radius) / viscosity


def get_drag_coefficient(Re):
    Cd_values = np.linspace(0.5, 0.35, 100)
    Re_values = np.linspace(5e4, 9e4, 100)
    return np.interp(Re, Re_values, Cd_values)


def get_drag_force(rho, A, Cd, speed, vel):
    Fd = 0.5 * rho * A * Cd * (speed ** 2) * vel / speed
    return Fd


def get_lift_force_magnus(spin_rate, circumference, rho, A, club_loft):
    spin_rate_decay_per_second = (spin_rate / 60) * circumference
    lift_force_magnus = 0.5 * rho * A * (spin_rate_decay_per_second ** 2) * math.sin(club_loft)
    return lift_force_magnus


class GolfBall:
    def __init__(self, mass=GOLF_BALL_MASS, radius=GOLF_BALL_RADIUS):
        self.mass = mass
        self.radius = radius


class Simulation:
    def __init__(self, golf_ball, club_mass, lift, club_velocity, club_loft):
        self.golf_ball = golf_ball
        self.club_mass = club_mass
        self.lift = lift
        self.club_velocity = club_velocity
        self.club_loft = club_loft

    def run(self):
        # Initialize variables
        pos = np.array([0.0, 0.0])
        vel = get_vel(CLUB_VELOCITY, CLUB_MASS, CLUB_LOFT, GOLF_BALL_MASS)
        spin_rate = SPIN_RATE_DECAY_PER_SECOND

        # Time step
        dt = 0.1

        # Number of loops
        n_loops = 200

        # Lists to store position data
        x_positions = [0]
        y_positions = [0]

        clock = pygame.time.Clock()

        while pos[1] >= 0 and 0 <= pos[0] <= screen_width and n_loops < 1000:
            # Calculate forces
            speed = np.linalg.norm(vel)
            Re = get_reynolds_number(AIR_DENSITY, self.golf_ball.radius, speed, KINEMATIC_VISCOSITY)
            Cd = get_drag_coefficient(Re)
            Fd = get_drag_force(AIR_DENSITY, GOLF_BALL_A, Cd, speed, vel)
            lift_force_magnus = get_lift_force_magnus(spin_rate, CIRCUMFERENCE, AIR_DENSITY, self.golf_ball.radius,
                                                      self.club_loft)
            net_lift = self.lift + lift_force_magnus
            spin_rate *= 0.999
            # Update acceleration
            acc = np.array([-Fd[0] / self.golf_ball.mass, GRAVITY + net_lift / self.golf_ball.mass])

            # Update velocity
            vel += acc * dt

            # Update position
            pos = pos + vel * dt + 0.5 * acc * (dt ** 2)

            x_positions.append(pos[0])
            y_positions.append(pos[1])

            screen.fill((0, 0, 0))

            # Draw the ball
            pygame.draw.circle(screen, (255, 255, 255), (int(pos[0] * 2), int(screen_height - pos[1] * 2)),
                               int(self.golf_ball.radius * 100))

            pygame.display.flip()
            clock.tick(60)

            # Update loop counter
            n_loops += 1

        # Print the maximum height and total x distance traveled
        max_height = max(y_positions)
        total_x_distance = sum(np.diff(x_positions))
        print(f"Maximum height: {max_height / 0.9144:.2f} yards")
        print(f"Total x distance traveled: {total_x_distance}")
        print(f"Total Distance: {total_x_distance / 0.9144:.2f} yards")


def main():
    # Create a golf ball object
    golf_ball = GolfBall()

    # Create a simulation object
    simulation = Simulation(golf_ball, CLUB_MASS, LIFT, CLUB_VELOCITY, CLUB_LOFT)

    for _ in range(50000):
        # Run the simulation
        simulation.run()


# Initialize Pygame
pygame.init()
# Create a display window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

if __name__ == '__main__':
    main()
import numpy as np
import matplotlib.pyplot as plt

# Club Properties
CLUB_VELOCITY = 34  # Impact velocity in m/s
CLUB_LOFT = np.radians(14)  # Impact angle in radians from degrees
CLUB_MASS = 0.22  # Impact mass in kg

# Ball Constants
m = 0.045  # mass of the ball (kg)
r = 0.021  # radius of the ball (m)
A = np.pi * r ** 2  # cross-sectional area (m^2)
Cd = 0.15  # drag coefficient
s = 0.000005  # magnus coefficient

# Environment Properties
g = 9.81  # acceleration due to gravity (m/s^2)
rho = 1.225  # air density (kg/m^3)

# Initial Conditions
W = -(CLUB_MASS * CLUB_VELOCITY * np.sin(CLUB_LOFT)) / (m * r) # Angular velocity
v0 = CLUB_VELOCITY  # initial velocity in m/s
vx0 = v0 * np.cos(CLUB_LOFT)  # initial x-velocity in m/s
vy0 = v0 * np.sin(CLUB_LOFT)  # initial y-velocity in m/s


# Time points
dt = 0.1
t_end = 10
n_steps = int(t_end / dt)
t = np.linspace(0, t_end, n_steps)

# Initialize arrays to store results
state = np.zeros((n_steps, 4))

# Set initial conditions
state[0] = [0, 0, vx0, vy0]

# Solve ODE using Euler's method
for i in range(n_steps - 1):
    x, y, vx, vy = state[i]

    FD = 0.5 * Cd * rho * A * (vx ** 2 + vy ** 2)  # Drag Force
    FM_x = s * W * vy  # Magnus force in x direction
    FM_y = -s * W * vx  # Magnus force in y direction

    state[i + 1] = state[i] + dt * np.array([
        vx,
        vy,
        -FD / m * vx + FM_x / m,
        -g - FD / m * vy + FM_y / m])

    if y < 0:
        break

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(state[:, 0], state[:, 1], label='Ball')
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('Golf Ball Flight Trajectory')
plt.grid()
plt.legend()
plt.ylim(0, None)  # Set the y-axis limit to start at 0
plt.gca().set_aspect('equal')
plt.show()
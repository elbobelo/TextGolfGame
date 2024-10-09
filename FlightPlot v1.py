import numpy as np
import matplotlib.pyplot as plt

# Ball Properties
m = 0.04593  # mass of the ball (kg)
r = 0.021335  # radius of the ball (m)
A = np.pi * r ** 2  # cross-sectional area (m^2)
Cd = 0.15  # drag coefficient
s = 0.000005  # magnus coefficient

# Environment Properties
g = 9.81  # acceleration due to gravity (m/s^2)
rho = 1.225  # air density (kg/m^3)

# Initial Conditions
v0 = 146.68  # initial velocity (m/s)
theta_degrees = 14.54  # initial angle (degrees)
theta = np.radians(theta_degrees)  # initial angle (radians)
vx0 = v0 * np.cos(theta)  # initial x-velocity
vy0 = v0 * np.sin(theta)  # initial y-velocity
W = -5000  # angular velocity (rad/s)

# Time points
dt = 0.01
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

# Plot results
plt.figure(figsize=(10, 4))
plt.plot(state[:, 0], state[:, 1], label='Ball')
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('Golf Ball Flight Trajectory')
plt.grid()
plt.legend()
plt.ylim(0, None)  # Set the y-axis limit to start at 0
plt.gca().set_aspect('equal')
plt.show()
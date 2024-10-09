import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
g = 9.8  # Acceleration due to gravity (m/s^2)
L1 = 1.0  # Length of the first pendulum (m)
L2 = 1.1  # Length of the second pendulum (m)
M1 = 1.0  # Mass of the first pendulum (kg)
M2 = .22  # Mass of the second pendulum (kg)

# Initial conditions
theta1_deg = -140  # Initial angle of the first pendulum (degrees)
theta2_deg = -220  # Initial angle of the second pendulum (degrees)
omega1 = 1.0  # Initial angular velocity of the first pendulum (rad/s)
omega2 = 0.0  # Initial angular velocity of the second pendulum (rad/s)

# Convert angles from degrees to radians
theta1 = np.deg2rad(theta1_deg)
theta2 = np.deg2rad(theta2_deg)

# Time variables
dt = 0.05  # Time step (s)
t = 0.0  # Time (s)
tf = 10.0  # Total time (s)

# Simulation arrays
theta1_values = []
theta2_values = []

# Animation function
def animate(frame):
    global t, theta1, theta2, omega1, omega2

    # Calculate accelerations
    a1 = (-g * (2 * M1 + M2) * np.sin(theta1) - M2 * g * np.sin(2 * theta1 + theta2) - 2 * np.sqrt(M1 * M2) * g * np.sin(theta1 + theta2) * np.cos(theta1 - theta2) - M2 * L2 * omega2**2 * np.sin(theta1 - 2 * theta2)) / (L1 * (2 * M1 + M2 - M2 * np.cos(2 * (theta1 - theta2)) ** 2))
    a2 = (2 * np.sqrt(M1 * M2) * g * np.sin(theta1 + theta2) + L2 * omega2**2 * np.sin(theta1 - theta2) + g * (M1 + M2) * np.cos(theta1 + theta2) + a1 * L1 * np.cos(theta1 - theta2)) / (L2 * (M1 + M2 - M2 * np.cos(2 * (theta1 - theta2)) ** 2))

    # Update angular velocities
    omega1 += a1 * dt
    omega2 += a2 * dt

    # Update angles
    theta1 += omega1 * dt
    theta2 += omega2 * dt

    # Append angles to arrays
    theta1_values.append(theta1)
    theta2_values.append(theta2)

    # Increase time
    t += dt

    # Check if the simulation has finished
    if t > tf:
        return

    # Plot the pendulums
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = L1 * np.sin(theta1) + L2 * np.sin(theta2)
    y2 = -L1 * np.cos(theta1) - L2 * np.cos(theta2)
    plt.plot(x1, y1, 'ro', x2, y2, 'bo')
    plt.xlim(-2.5, 2.5)
    plt.ylim(-2.5, 2.5)
    plt.pause(0.001)

# Initialize the plot
fig, ax = plt.subplots()

# Start the animation
ani = FuncAnimation(fig, animate, interval=20)
plt.show()
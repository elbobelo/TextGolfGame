import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

# --- Function to calculate and plot flight ---
def calculate_flight():
    try:
        # Get input values and validate
        inputs = {}
        for label, entry in entries.items():
            try:
                inputs[label] = float(entry.get())
                if inputs[label] <= 0:  # Validate for positive values
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", f"Invalid input for '{label}'. Please enter a positive number.")
                return

        # Extract values from the dictionary for clarity
        club_velocity = inputs["Club Velocity (m/s):"]
        club_loft = np.radians(inputs["Club Loft (degrees):"])
        club_mass = inputs["Club Mass (kg):"]
        lift = inputs["Lift Coefficient:"]
        golf_ball_mass = inputs["Golf Ball Mass (kg):"]
        golf_ball_radius = inputs["Golf Ball Radius (m):"]
        air_density = inputs["Air Density (kg/m^3):"]
        kinematic_viscosity = inputs["Kinematic Viscosity (m^2/s):"]

        # Calculate ball properties
        golf_ball_area = np.pi * golf_ball_radius**2
        circumference = 2 * np.pi * golf_ball_radius
        vertical_velocity = club_velocity * np.sin(club_loft)
        spin_rate_decay_per_second = vertical_velocity / circumference / 60

        # Trajectory simulation (Simplified example, replace with your model)
        g = 9.81

        # Calculate ball properties (including Reynolds number and drag coefficient)
        golf_ball_area = np.pi * golf_ball_radius ** 2
        circumference = 2 * np.pi * golf_ball_radius
        vertical_velocity = club_velocity * np.sin(club_loft)
        spin_rate = vertical_velocity / circumference  # Initial spin rate

        reynolds_number = (golf_ball_radius * 2 * club_velocity) / kinematic_viscosity
        drag_coefficient = 0.5  # Placeholder, replace with your actual drag model

        # Calculate initial ball velocity using energy transfer and impact
        coefficient_of_restitution = 0.8  # Typical value for golf club/ball impact
        club_head_velocity = math.sqrt((2 * club_velocity ** 2 * club_mass) / (club_mass + golf_ball_mass))
        initial_ball_velocity = (1 + coefficient_of_restitution) * club_head_velocity * (club_mass / (club_mass + golf_ball_mass))

        # Trajectory simulation with Magnus effect and drag
        g = 9.81
        dt = 0.01  # Time step
        t = 0
        x, y, vx, vy, spin_rate = 0, 0, initial_ball_velocity * np.cos(club_loft), initial_ball_velocity * np.sin(club_loft), initial_ball_velocity / circumference  # Initial spin rate
        x_positions, y_positions = [], []

        while y >= 0:  # Stop when the ball hits the ground (y = 0)
            # Calculate forces
            drag_force = 0.5 * drag_coefficient * air_density * golf_ball_area * vx ** 2
            lift_force_magnus = 0.5 * lift * air_density * golf_ball_area * (spin_rate * golf_ball_radius) ** 2

            # Update velocities
            ax = -drag_force / golf_ball_mass
            ay = -g + lift_force_magnus / golf_ball_mass

            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt

            # Spin decay (adjust model as needed)
            spin_rate *= (1 - spin_rate_decay_per_second * dt)

            # Store positions
            x_positions.append(x)
            y_positions.append(y)

            t += dt

        # Clear the figure (not the axis) before plotting
        fig.clf()

        # Re-create the axis and plot the new trajectory
        ax = fig.add_subplot(111)
        ax.plot(x_positions, y_positions, marker='o', linestyle='-', color='blue')  # Markers for points, solid line

        # Set equal aspect ratio for x and y axes
        ax.set_aspect('equal', adjustable='box')  # 'box' ensures equal scaling regardless of plot size

        # Ensure x and y limits are the same to maintain equal spacing
        max_value = max(max(x_positions), max(y_positions))
        ax.set_xlim([0, max_value])
        ax.set_ylim([0, max_value])

        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Height (m)")
        ax.set_title("Golf Ball Trajectory")
        ax.grid(True)

        # Update the canvas to show the new plot
        canvas.draw()

    except ValueError:
        tk.messagebox.showerror("Error", "Invalid input. Please enter numbers only.")

# --- Create the main window and widgets ---
root = tk.Tk()
root.title("Golf Ball Flight Simulator")

# Input Frame
input_frame = ttk.LabelFrame(root, text="Input Parameters")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Input Fields with Labels and Entry Widgets
entries = {}  # Dictionary to store entry widgets
input_fields = [
    ("Club Velocity (m/s):", tk.StringVar(value=34)),
    ("Club Loft (degrees):", tk.StringVar(value=14)),
    ("Club Mass (kg):", tk.StringVar(value=0.22)),
    ("Lift Coefficient:", tk.StringVar(value=0.4)),
    ("Golf Ball Mass (kg):", tk.StringVar(value=0.04593)),
    ("Golf Ball Radius (m):", tk.StringVar(value=0.021335)),
    ("Air Density (kg/m^3):", tk.StringVar(value=1.225)),
    ("Kinematic Viscosity (m^2/s):", tk.StringVar(value="1.8e-5"))  # Scientific notation
]

for i, (label_text, entry_var) in enumerate(input_fields):
    ttk.Label(input_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = ttk.Entry(input_frame, textvariable=entry_var)
    entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
    entries[label_text] = entry  # Store the entry widget


# Plot frame
plot_frame = ttk.LabelFrame(root, text="Trajectory Plot")
plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Matplotlib figure and canvas
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

# Calculate button
calculate_button = ttk.Button(root, text="Calculate", command=calculate_flight)
calculate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Assign entry widgets to variables after they've been created
club_velocity_entry = entries["Club Velocity (m/s):"]
club_loft_entry = entries["Club Loft (degrees):"]
club_mass_entry = entries["Club Mass (kg):"]
lift_entry = entries["Lift Coefficient:"]
golf_ball_mass_entry = entries["Golf Ball Mass (kg):"]
golf_ball_radius_entry = entries["Golf Ball Radius (m):"]
air_density_entry = entries["Air Density (kg/m^3):"]
kinematic_viscosity_entry = entries["Kinematic Viscosity (m^2/s):"]

root.mainloop()
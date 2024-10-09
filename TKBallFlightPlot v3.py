import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math


class GolfSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Golf Ball Flight Simulator")

        self.physics_engine = PhysicsEngine()
        self.trajectory_plotter = TrajectoryPlotter(master)

        self._create_input_frame()  # Create the input frame with pre-populated values
        self._create_calculate_button()

    def _create_input_frame(self):
        self.input_frame = ttk.LabelFrame(self.master, text="Input Parameters")
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.entries = {}
        input_fields = [
            ("Golf Ball Mass (kg):", "0.04593"),
            ("Golf Ball Radius (m):", "0.021335"),
            ("Club Velocity (m/s):", "34"),
            ("Club Loft (degrees):", "14"),
            ("Club Mass (kg):", "0.22"),
            ("Air Temperature (Celsius):", "20"),
            ("Altitude (meters):", "0.1"),  # New field with default 0 (sea level)
            ("Humidity (%):", "50")      # New field with default 50%
        ]

        for i, (label_text, default_value) in enumerate(input_fields):
            ttk.Label(self.input_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry_var = tk.StringVar(value=default_value)
            entry = ttk.Entry(self.input_frame, textvariable=entry_var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[label_text] = entry_var

    def _create_calculate_button(self):
        calculate_button = ttk.Button(self.master, text="Calculate", command=self._calculate_flight)
        calculate_button.grid(row=1, column=1, padx=10, pady=10)

    def _calculate_flight(self):
        try:
            inputs = {label: float(entry.get()) for label, entry in self.entries.items()}
            if any(value <= 0 for value in inputs.values()):
                raise ValueError

            trajectory_data = self.physics_engine.calculate_trajectory(inputs)
            self.trajectory_plotter.plot_trajectory(trajectory_data)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter positive numbers only.")


class PhysicsEngine:
    def calculate_trajectory(self, inputs):
        # Constants
        g = 9.81  # Acceleration due to gravity
        dt = 0.01  # Time step for simulation
        R = 287.058  # Specific gas constant for dry air
        T_ref = 273.15  # Reference temperature in Kelvin
        mu_ref = 1.716e-5  # Reference dynamic viscosity at T_ref
        S = 110.4  # Sutherland's constant for air

        # Extract input values
        golf_ball_mass = inputs["Golf Ball Mass (kg):"]
        golf_ball_radius = inputs["Golf Ball Radius (m):"]
        club_velocity = inputs["Club Velocity (m/s):"]
        club_loft = np.radians(inputs["Club Loft (degrees):"])
        club_mass = inputs["Club Mass (kg):"]
        air_temperature = inputs["Air Temperature (Celsius):"]
        altitude = inputs["Altitude (meters):"]
        humidity = inputs["Humidity (%):"] / 100  # Convert to fraction

        # Ball properties
        golf_ball_area = np.pi * golf_ball_radius**2
        circumference = 2 * np.pi * golf_ball_radius
        vertical_velocity = club_velocity * np.sin(club_loft)
        lift = 0.4  # Default lift coefficient (can be adjusted if needed)
        coefficient_of_restitution = 0.8  # Typical value for golf club/ball impact
        spin_rate_decay_per_second = vertical_velocity / circumference / 60

        # Calculate initial ball velocity using energy transfer and impact
        club_head_velocity = math.sqrt((2 * club_velocity ** 2 * club_mass) / (club_mass + golf_ball_mass))
        initial_ball_velocity = (1 + coefficient_of_restitution) * club_head_velocity * (club_mass / (club_mass + golf_ball_mass))

        # Trajectory simulation with Magnus effect and drag
        t = 0
        x, y, vx, vy, spin_rate = 0, 0, initial_ball_velocity * np.cos(club_loft), initial_ball_velocity * np.sin(club_loft), initial_ball_velocity / circumference
        x_positions, y_positions = [], []

        while y >= 0:
            # Update altitude-dependent properties within the loop
            altitude = y  # Current altitude is the ball's height

            # Calculate air pressure based on altitude (International Standard Atmosphere model)
            temp_kelvin = air_temperature + T_ref
            pressure = 101325 * (1 - 2.25577e-5 * altitude) ** 5.25588

            # Adjust air density for humidity (simplified approximation)
            saturation_vapor_pressure = 6.1078 * 10**(7.5 * air_temperature / (237.3 + air_temperature))
            vapor_pressure = humidity * saturation_vapor_pressure
            air_density = (pressure - vapor_pressure) / (R * temp_kelvin)

            # Calculate kinematic viscosity based on air temperature (Sutherland's formula)
            kinematic_viscosity = (mu_ref * ((T_ref + air_temperature) / T_ref)
                                   ** 1.5 * T_ref / ((T_ref + air_temperature) + S))

            # Calculate forces
            reynolds_number = (golf_ball_radius * 2 * math.sqrt(vx**2 + vy**2)) / kinematic_viscosity

            # Calculate drag coefficient based on the Reynolds number (rough approximation)
            if reynolds_number < 1:  # Stokes' Law regime
                drag_coefficient = 24 / reynolds_number
            elif reynolds_number < 2.3e5:  # Laminar flow regime
                drag_coefficient = (24 / reynolds_number) * (1 + 0.14 * reynolds_number**0.7)
            else:  # Turbulent flow regime
                drag_coefficient = 0.47  # Golf ball drag coefficient in turbulent flow

            drag_force = (0.5 * drag_coefficient * air_density
                          * golf_ball_area * math.sqrt(vx**2 + vy**2) * vx)  # Drag acts in the direction of velocity
            lift_force_magnus = 0.5 * lift * air_density * golf_ball_area * (spin_rate * golf_ball_radius) ** 2
            print(spin_rate)
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

        return x_positions, y_positions


class TrajectoryPlotter:
    def __init__(self, master):
        self.plot_frame = ttk.LabelFrame(master, text="Trajectory Plot")
        self.plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack()

    def plot_trajectory(self, trajectory_data):
        x_positions, y_positions = trajectory_data  # Unpack the tuple

        self.ax.clear()  # Clear previous plot
        self.ax.plot(x_positions, y_positions, marker='o', linestyle='-', color='blue')

        # Set equal aspect ratio and appropriate limits for a clear visualization
        max_value = max(max(x_positions), max(y_positions)) * 1.1  # Add a 10% buffer
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlim([0, max_value])
        self.ax.set_ylim([0, max_value])

        self.ax.set_xlabel("Distance (m)")
        self.ax.set_ylabel("Height (m)")
        self.ax.set_title("Golf Ball Trajectory")
        self.ax.grid(True)

        self.canvas.draw()  # Update the plot


# --- Run the application ---
root = tk.Tk()
GolfSimulator(root)
root.mainloop()
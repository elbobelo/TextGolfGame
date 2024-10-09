import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


def double_pendulum_deriv(t, z, g, m1, m2, l1, l2):
    """Computes the derivatives for the double pendulum system."""
    z1, z2, z3, z4 = z
    sin_diff = np.sin(z1 - z3)
    cos_diff = np.cos(z1 - z3)
    den1 = 2 * l1 * (m1 + m2 - m2 * cos_diff**2)
    den2 = l2 * (m1 + m2 - m2 * cos_diff**2)

    dz1dt = z2
    dz2dt = -((g * (2 * m1 + m2) * np.sin(z1) + m2 * (g * np.sin(z1 - 2 * z3) + 2 * (l2 * z4**2 + l1 * z2**2 * cos_diff) * sin_diff)) / den1)
    dz3dt = z4
    dz4dt = (((m1 + m2) * (l1 * z2**2 + g * np.cos(z1)) + l2 * m2 * z4**2 * cos_diff) * sin_diff) / den2

    return dz1dt, dz2dt, dz3dt, dz4dt


def simulate_double_pendulum(frame, g, m1, m2, l1, l2, z0, duration):
    """Simulates the double pendulum and updates the animation."""
    dt = 0.05
    t = np.arange(0, duration, dt)

    if frame == 0:
        z = np.zeros((len(t), 4))
        z[0] = z0

        for i in range(1, len(t)):
            dzdt = np.array(double_pendulum_deriv(t[i - 1], z[i - 1], g, m1, m2, l1, l2))
            z[i] = z[i - 1] + dzdt * dt
        simulate_double_pendulum.z = z

    x1 = l1 * np.sin(simulate_double_pendulum.z[:, 0])
    y1 = -l1 * np.cos(simulate_double_pendulum.z[:, 0])
    x2 = x1 + l2 * np.sin(simulate_double_pendulum.z[:, 2])
    y2 = y1 - l2 * np.cos(simulate_double_pendulum.z[:, 2])

    line.set_data([0, x1[frame], x2[frame]], [0, y1[frame], y2[frame]])
    time_text.set_text(f"Time: {t[frame]:.2f}s")
    return line, time_text


def start_animation():
    """Starts or restarts the animation with updated parameters."""
    global ani

    # Stop the existing animation, if any
    if ani and ani.event_source is not None:  # Check both ani and event_source
        ani.event_source.stop()

    # Clear existing plot
    ax.clear()
    ax.set_xlim(-(float(l1_entry.get()) + float(l2_entry.get())), float(l1_entry.get()) + float(l2_entry.get()))
    ax.set_ylim(-(float(l1_entry.get()) + float(l2_entry.get())), float(l1_entry.get()) + float(l2_entry.get()))

    # Redraw plot elements
    global line, time_text
    line, = ax.plot([], [], 'o-', lw=2)
    time_text = ax.text(0.05, 0.9, "", transform=ax.transAxes)

    g = float(g_entry.get())
    m1 = float(m1_entry.get())
    m2 = float(m2_entry.get())
    l1 = float(l1_entry.get())
    l2 = float(l2_entry.get())
    z0 = [
        np.radians(float(theta1_entry.get())),
        float(dtheta1_entry.get()),
        np.radians(float(theta2_entry.get())),
        float(dtheta2_entry.get())
    ]
    duration = float(duration_entry.get())

    # Create a new FuncAnimation with updated parameters
    ani = animation.FuncAnimation(
        fig,
        simulate_double_pendulum,
        fargs=(g, m1, m2, l1, l2, z0, duration),
        frames=int(duration / 0.05),
        interval=50,
        blit=True,
        repeat=False,
    )

    canvas.draw()


# --- Tkinter GUI ---
window = tk.Tk()
window.title("Double Pendulum Simulation")

# Animation frame
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
ax.set_aspect('equal')
ax.grid()
line, = ax.plot([], [], 'o-', lw=2)
time_text = ax.text(0.05, 0.9, "", transform=ax.transAxes)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Control frame
control_frame = tk.Frame(window)
control_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

labels = ["g (m/s^2)", "m1 (kg)", "m2 (kg)", "l1 (m)", "l2 (m)", "theta1 (deg)", "dtheta1 (deg/s)", "theta2 (deg)", "dtheta2 (deg/s)", "Duration (s)"]
entries = []
for label in labels:
    tk.Label(control_frame, text=label).pack()
    entry = tk.Entry(control_frame)
    entry.pack()
    entries.append(entry)

g_entry, m1_entry, m2_entry, l1_entry, l2_entry, theta1_entry, dtheta1_entry, theta2_entry, dtheta2_entry, duration_entry = entries

# Default values
g_entry.insert(0, "9.81")
m1_entry.insert(0, "1")
m2_entry.insert(0, "1")
l1_entry.insert(0, "2")
l2_entry.insert(0, "1")
theta1_entry.insert(0, "210")  # Small perturbation
dtheta1_entry.insert(0, "0")
theta2_entry.insert(0, "0")
dtheta2_entry.insert(0, "0")
duration_entry.insert(0, "50")

start_button = tk.Button(control_frame, text="Start", command=start_animation)
start_button.pack()

ani = None

window.mainloop()
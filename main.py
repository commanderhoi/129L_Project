import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Function to simulate the motion of a double pendulum
def double_pendulum(t, y, l1, l2, m1, m2, g):
    theta1, omega1, theta2, omega2 = y

    # Equations of motion
    dydt = [omega1,
            (-g * (2 * m1 + m2) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2 * theta2)
             - 2 * np.sin(theta1 - theta2) * m2 * (omega2 ** 2 * l2 + omega1 ** 2 * l1 * np.cos(theta1 - theta2)))
            / (l1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2))),
            omega2,
            (2 * np.sin(theta1 - theta2) * (omega1 ** 2 * l1 * (m1 + m2) + g * (m1 + m2) * np.cos(theta1)
                                            + omega2 ** 2 * l2 * m2 * np.cos(theta1 - theta2)))
            / (l2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))]

    return dydt

# Set up the plot
fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])

# Define parameters
l1 = 1.0  # length of the first pendulum
l2 = 1.0  # length of the second pendulum
m1 = 1.0  # mass of the first pendulum
m2 = 1.0  # mass of the second pendulum
g = 9.8   # acceleration due to gravity

# Number of pendulums
num_pendulums = 2

# List to store pendulum data
pendulums = []

# Define the time span for the simulation
t_span = (0, 10)  # Replace 0 and 10 with the start and end times of your simulation
t_step = 0.01

# Create a list of unique colors for each pendulum
pendulum_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Initialize lines for each pendulum
lines = []

# Create pendulums with initial conditions and colors
for i in range(num_pendulums):
    initial_conditions = np.random.rand(4) * 2 * np.pi  # Random initial conditions
    pendulum_data = {
        'initial_conditions': initial_conditions,
        'x1': None,
        'y1': None,
        'x2': None,
        'y2': None,
    }
    pendulums.append(pendulum_data)

    # Initialize lines for the current pendulum
    line1, = ax.plot([], [], lw=2, marker='o', markersize=6, color=pendulum_colors[i])
    line2, = ax.plot([], [], lw=2, marker='o', markersize=6, color=pendulum_colors[i])
    lines.append((line1, line2))

# Initialize center label
center_label = ax.text(0, 0, 'Center', fontsize=10, ha='center', va='center')

# Initialize labels for each pendulum
pendulum_labels = []
for i in range(num_pendulums):
    pendulum_label = ax.text(0, 0, f'Pendulum {i + 1}', fontsize=10, ha='center', va='center')
    pendulum_labels.append(pendulum_label)

# Function to update the plot in animation
def update_plot(frame):
    # Update lines for each pendulum
    for i, line in enumerate(lines):
        pendulum = pendulums[i]
        pendulum_line1, pendulum_line2 = line
        pendulum_line1.set_data([0, pendulum['x1'][frame], pendulum['x2'][frame]],
                                [0, pendulum['y1'][frame], pendulum['y2'][frame]])
        pendulum_line2.set_data([pendulum['x1'][frame], pendulum['x2'][frame]],
                                [pendulum['y1'][frame], pendulum['y2'][frame]])

    # Update center label
    center_label.set_position((0, 0))

    # Update labels for each pendulum
    for i, pendulum_label in enumerate(pendulum_labels):
        pendulum_data = pendulums[i]
        pendulum_label.set_position((pendulum_data['x2'][frame], pendulum_data['y2'][frame]))

    # Pause for a short duration
    plt.pause(t_step)

# Solve ODEs for each pendulum
for i in range(num_pendulums):
    sol = solve_ivp(
        double_pendulum,
        t_span,
        pendulums[i]['initial_conditions'],
        args=(l1, l2, m1, m2, g),
        t_eval=np.arange(t_span[0], t_span[1], t_step)
    )

    # Extract solution
    theta1, omega1, theta2, omega2 = sol.y

    # Convert polar coordinates to Cartesian coordinates
    pendulums[i]['x1'] = l1 * np.sin(theta1)
    pendulums[i]['y1'] = -l1 * np.cos(theta1)
    pendulums[i]['x2'] = pendulums[i]['x1'] + l2 * np.sin(theta2)
    pendulums[i]['y2'] = pendulums[i]['y1'] - l2 * np.cos(theta2)
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the double pendulum system
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


# Function to update the plot in animation
def update_plot(frame, pendulum_line1, pendulum_line2):
    pendulum_line1.set_data([0, x1[frame], x2[frame]], [0, y1[frame], y2[frame]])
    pendulum_line2.set_data([x1[frame], x2[frame]], [y1[frame], y2[frame]])
    return pendulum_line1, pendulum_line2


# Set up initial conditions and parameters
l1 = 1.0  # length of the first pendulum
l2 = 1.0  # length of the second pendulum
m1 = 1.0  # mass of the first pendulum
m2 = 1.0  # mass of the second pendulum
g = 9.8  # acceleration due to gravity

# Initial conditions: theta1, omega1, theta2, omega2
initial_conditions = [np.pi / 4, 0, np.pi / 2, 0]

# Time span and step for the simulation
t_span = (0, 10)
t_step = 0.05

# Solve the ODEs using solve_ivp
sol = solve_ivp(
    double_pendulum,
    t_span,
    initial_conditions,
    args=(l1, l2, m1, m2, g),
    t_eval=np.arange(t_span[0], t_span[1], t_step)
)

# Extract the solution
theta1, omega1, theta2, omega2 = sol.y

# Convert polar coordinates to Cartesian coordinates
x1 = l1 * np.sin(theta1)
y1 = -l1 * np.cos(theta1)
x2 = x1 + l2 * np.sin(theta2)
y2 = y1 - l2 * np.cos(theta2)

# Set up the plot and animation
fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='datalim')
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])

pendulum_line1, = ax.plot([], [], lw=2, marker='o', markersize=6)
pendulum_line2, = ax.plot([], [], lw=2, marker='o', markersize=6)

animation = FuncAnimation(
    fig,
    update_plot,
    frames=len(sol.t),
    fargs=(pendulum_line1, pendulum_line2),
    interval=t_step * 1000,
    blit=True
)

plt.show()

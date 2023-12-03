import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def double_pendulum(t, y, l1, l2, m1, m2, g):
    theta1, omega1, theta2, omega2 = y
    dydt = [omega1,
            (-g * (2 * m1 + m2) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2 * theta2)
             - 2 * np.sin(theta1 - theta2) * m2 * (omega2 ** 2 * l2 + omega1 ** 2 * l1 * np.cos(theta1 - theta2)))
            / (l1 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2))),
            omega2,
            (2 * np.sin(theta1 - theta2) * (omega1 ** 2 * l1 * (m1 + m2) + g * (m1 + m2) * np.cos(theta1)
                                            + omega2 ** 2 * l2 * m2 * np.cos(theta1 - theta2)))
            / (l2 * (2 * m1 + m2 - m2 * np.cos(2 * theta1 - 2 * theta2)))]
    return dydt

def update_plot(frame, pendulum_line1, pendulum_line2, path_line):
    pendulum_line1.set_data([0, global_x1[frame], global_x2[frame]], [0, global_y1[frame], global_y2[frame]])
    pendulum_line2.set_data([global_x1[frame], global_x2[frame]], [global_y1[frame], global_y2[frame]])
    path_line.set_data(global_x2[:frame + 1], global_y2[:frame + 1])
    return pendulum_line1, pendulum_line2, path_line

def d_pendulum_sim(l1, l2, m1, m2, theta_1, omega_1, theta_2, omega_2, t_span, t_step):
    global global_x1, global_y1, global_x2, global_y2

    # Solve the ODEs using solve_ivp
    sol = solve_ivp(
        double_pendulum,
        t_span,
        [theta_1, omega_1, theta_2, omega_2],
        args=(l1, l2, m1, m2, 9.8),
        t_eval=np.arange(t_span[0], t_span[1], t_step)
    )

    # Extract the solution
    theta1, omega1, theta2, omega2 = sol.y

    # Convert polar coordinates to Cartesian coordinates
    global_x1 = l1 * np.sin(theta1)
    global_y1 = -l1 * np.cos(theta1)
    global_x2 = global_x1 + l2 * np.sin(theta2)
    global_y2 = global_y1 - l2 * np.cos(theta2)

    # Set up the plot and animation
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim([-2.5, 2.5])
    ax.set_ylim([-2.5, 2.5])
    ax.set_title("Double Pendulum Simulation")

    pendulum_line1, = ax.plot([], [], lw=2, marker='o', markersize=6)
    pendulum_line2, = ax.plot([], [], lw=2, marker='o', markersize=6)

    # Initialize the path line for mass 2
    path_line, = ax.plot([], [], lw=1, color='red')

    animation = FuncAnimation(
        fig,
        update_plot,
        frames=len(sol.t),
        fargs=(pendulum_line1, pendulum_line2, path_line),
        interval=t_step * 1000,
        blit=True
    )

    plt.show()

# Example usage:
d_pendulum_sim(1.0, 1.0, 1.0, 1.0, np.pi / 4, 0, np.pi / 4, 0, (0, 60), 0.010)
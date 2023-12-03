import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def triple_pendulum(t, y, l1, l2, l3, m1, m2, m3, g):
    theta1, omega1, theta2, omega2, theta3, omega3 = y

    # Equations of motion
    dydt = [omega1,
            (-g * (2 * m1 + m2 + m3) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2 * theta2)
             - m3 * g * np.sin(theta1 - 2 * theta3) - 2 * np.sin(theta1 - theta2) * m2 * (omega2 ** 2 * l2 + omega1 ** 2 * l1 * np.cos(theta1 - theta2))
             - 2 * np.sin(theta1 - theta3) * m3 * (omega3 ** 2 * l3 + omega1 ** 2 * l1 * np.cos(theta1 - theta3)))
            / (l1 * (2 * m1 + m2 + m3 - m2 * np.cos(2 * theta1 - 2 * theta2) - m3 * np.cos(2 * theta1 - 2 * theta3))),
            omega2,
            (-g * (2 * m1 + m2 + m3) * np.sin(theta2) - m3 * g * np.sin(theta2 - 2 * theta3)
             - 2 * np.sin(theta2 - theta1) * (m1 + m3) * (omega1 ** 2 * l1 + g * np.cos(theta1) + omega3 ** 2 * l3 * np.cos(theta2 - theta3))
             - 2 * np.sin(theta2 - theta3) * m3 * (omega3 ** 2 * l3 + omega2 ** 2 * l2 * np.cos(theta2 - theta3)))
            / (l2 * (2 * m1 + m2 + m3 - m1 * np.cos(2 * theta2 - 2 * theta1) - m3 * np.cos(2 * theta2 - 2 * theta3))),
            omega3,
            (-g * (2 * m1 + m2 + m3) * np.sin(theta3) - 2 * np.sin(theta3 - theta1) * (m1 + m2) * (omega1 ** 2 * l1 + g * np.cos(theta1))
             - 2 * np.sin(theta3 - theta2) * (m2 + m1) * (omega2 ** 2 * l2 + g * np.cos(theta2))
             - 2 * np.sin(theta3 - theta2) * m3 * (omega3 ** 2 * l3 + omega2 ** 2 * l2 * np.cos(theta2 - theta3)))
            / (l3 * (2 * m1 + m2 + m3 - m1 * np.cos(2 * theta3 - 2 * theta1) - m2 * np.cos(2 * theta3 - 2 * theta2)))]

    return dydt

def update_triple_pendulum(frame, pendulum_line1, pendulum_line2, pendulum_line3, path_line1, path_line2, path_line3):
    pendulum_line1.set_data([0, x1[frame], x2[frame], x3[frame]], [0, y1[frame], y2[frame], y3[frame]])
    pendulum_line2.set_data([x1[frame], x2[frame], x3[frame]], [y1[frame], y2[frame], y3[frame]])
    pendulum_line3.set_data([x2[frame], x3[frame]], [y2[frame], y3[frame]])

    # Update the paths
    path_line1.set_data(x1[:frame + 1], y1[:frame + 1])
    path_line2.set_data(x2[:frame + 1], y2[:frame + 1])
    path_line3.set_data(x3[:frame + 1], y3[:frame + 1])

    return pendulum_line1, pendulum_line2, pendulum_line3, path_line1, path_line2, path_line3

def triple_pendulum_sim(l1, l2, l3, m1, m2, m3, theta1, omega1, theta2, omega2, theta3, omega3, t_span, t_step):
    global x1, y1, x2, y2, x3, y3

    # Solve the ODEs for the triple pendulum
    sol = solve_ivp(
        triple_pendulum,
        t_span,
        [theta1, omega1, theta2, omega2, theta3, omega3],
        args=(l1, l2, l3, m1, m2, m3, 9.8),
        t_eval=np.arange(t_span[0], t_span[1], t_step)
    )

    # Extract the solution
    theta1, omega1, theta2, omega2, theta3, omega3 = sol.y
    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)
    x3 = x2 + l3 * np.sin(theta3)
    y3 = y2 - l3 * np.cos(theta3)

    # Set up the plot and animation
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim([-2.5, 2.5])
    ax.set_ylim([-2.5, 2.5])
    ax.set_title("Triple Pendulum Simulation")

    pendulum_line1, = ax.plot([], [], lw=2, marker='o', markersize=6, label='Pendulum 1')
    pendulum_line2, = ax.plot([], [], lw=2, marker='o', markersize=6, label='Pendulum 2')
    pendulum_line3, = ax.plot([], [], lw=2, marker='o', markersize=6, label='Pendulum 3')

    # Initialize path lines
    path_line1, = ax.plot([], [], lw=1, color='blue')
    path_line2, = ax.plot([], [], lw=1, color='green')
    path_line3, = ax.plot([], [], lw=1, color='red')

    animation = FuncAnimation(
        fig,
        update_triple_pendulum,
        frames=len(sol.t),
        fargs=(pendulum_line1, pendulum_line2, pendulum_line3, path_line1, path_line2, path_line3),
        interval=t_step * 1000,
        blit=True
    )

    plt.legend()
    plt.show()

# Example usage:
triple_pendulum_sim(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, np.pi / 4, 0, np.pi / 2, 0, 3 * np.pi / 4, 0, (0, 10), 0.010)
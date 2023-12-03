import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

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

def solve_double_pendulum(l1, l2, m1, m2, theta1, omega1, theta2, omega2, t_span, t_step):
    # Solve the ODEs for the double pendulum
    sol = solve_ivp(
        double_pendulum,
        t_span,
        [theta1, omega1, theta2, omega2],
        args=(l1, l2, m1, m2, 9.8),
        t_eval=np.arange(t_span[0], t_span[1], t_step)
    )

    # Extract the solution
    theta1, omega1, theta2, omega2 = sol.y
    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)

    return sol.t, x1, y1, x2, y2

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def compare_pendulum_simulations(l1, l2, m1, m2, theta1, omega1, theta2_1, omega2, theta2_2, t_span, t_step):
    # Solve the ODEs for the first pendulum
    t1, x1, y1, x2_1, y2_1 = solve_double_pendulum(l1, l2, m1, m2, theta1, omega1, theta2_1, omega2, t_span, t_step)

    # Solve the ODEs for the second pendulum with different initial condition (theta2_2)
    t2, x1, y1, x2_2, y2_2 = solve_double_pendulum(l1, l2, m1, m2, theta1, omega1, theta2_2, omega2, t_span, t_step)

    # Calculate the distance between masses for both pendulums at each time step
    errors = [calculate_distance(x2_1[i], y2_1[i], x2_2[i], y2_2[i]) for i in range(len(t1))]

    # Plot the error
    plt.plot(t1, errors, label='Error')
    plt.xlabel('Time')
    plt.ylabel('Distance Error')
    plt.legend()
    plt.title('Distance Error between Pendulum Systems')
    plt.show()

# Example usage:
compare_pendulum_simulations(1.0, 1.0, 1.0, 1.0, np.pi / 4, 0, np.pi / 4, 0, 3 * np.pi / 16, (0, 10), 0.010)

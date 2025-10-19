import matplotlib.pyplot as plt

def leapfrog(x_i : float, v_minushalf : float, dt : float, func) -> tuple:
    v_half = v_minushalf + dt *  func(x_i)
    x_new = x_i + dt * v_half
    return x_new, v_half

def harmonic_func(x):
    k_over_m = 2.0
    return -k_over_m * x

def pendulum_step(dt, x_initial, v_initial, v_minushalf_initial):
    x_positions = [x_initial]
    v_halfs = [v_minushalf_initial]
    x_new, v_half = leapfrog(x_initial, v_minushalf_initial, dt, harmonic_func)
    for steps in range(100):
        x_new, v_half = leapfrog(x_new, v_half, dt, harmonic_func)
        x_positions.append(x_new)
        v_halfs.append(v_half)
    return x_positions, v_halfs

xpos, v_halfs = pendulum_step(0.1, 1.0, 0.0, 0.1)

plt.plot(xpos,v_halfs)
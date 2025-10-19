def leapfrog(x_i : float, v_minushalf : float, dt : float, func) -> tuple:
    v_half = v_minushalf + dt *  func(x_i)
    x_new = x_i + dt * v_half
    return x_new, v_half

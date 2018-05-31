import numpy as np

class CrankNicholsonSolver:

    def __init__(self, initial_state, boundary_condition, timestep, grid_size,
                 start_grid=0, end_grid=1, start_time=0, end_time=1, max_iters=1000):
        self.initial_state = initial_state
        self.boundary_condition = boundary_condition
        self.timestep = timestep
        self.grid_size = grid_size
        self.start_grid = start_grid
        self.end_grid = end_grid
        self.start_time = start_time
        self.end_time = end_time
        self.max_iters = max_iters

    def step(self):
        iters = 0
        t0 = self.start_time
        tf = self.end_time
        x0 = self.start_grid
        xf = self.end_grid
        m = self.grid_size
        k = self.timestep
        h = (xf - x0) / (m )
        max_iters = self.max_iters
        t = t0
        u = self.initial_state
        g = self.boundary_condition
        grid_points = np.linspace(self.start_grid, self.end_grid, self.grid_size, endpoint=True)
        yield t, u
        iters += 1
        r = k / (2 * np.power(h, 2))
        print(h, k, r)
        A = np.diagflat(m * [-2]) + np.diagflat((m-1) * [1], k=-1) + np.diagflat((m-1) * [1], k=1)
        identity = np.identity(m)
        A1 = identity + r * A
        A2 = identity - r * A
        while t < tf and iters <= max_iters:
            t_old = t
            t = t0 + k * iters
            rhs = np.matmul(A1, u)
            rhs[0] += r * (g(x0, t_old) + g(x0, t))
            rhs[-1] += r * (g(xf, t_old) + g(xf, t))
            u = np.linalg.solve(A2, rhs)
            u[0] = g(x0, t)
            u[-1] = g(xf, t)
            yield t, u
            iters += 1

    __iter__ = step

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    start_grid = -1
    end_grid = 1
    grid_size = 2000
    timestep = 0.001
    grid = np.linspace(start_grid, end_grid, grid_size, endpoint=True)
#    initial_state = np.exp(-np.power(grid, 2))
    initial_state = np.array(grid_size * [0.0])
    boundary_condition = lambda x, t: (-x + 3.0) / 4.0
    initial_state[0] = boundary_condition(start_grid, 0)
    initial_state[-1] = boundary_condition(end_grid, 0)
    solver = CrankNicholsonSolver(initial_state, boundary_condition, timestep, grid_size,
                                  start_grid=start_grid, end_grid=end_grid,
                                  end_time=5)
    for t, u in solver:
        if np.abs((t % 1) - 0.5) * np.abs(t % 1) <= 0.0001:
            plt.plot(grid, u, '.-', label=t)
    plt.legend()
    plt.show()

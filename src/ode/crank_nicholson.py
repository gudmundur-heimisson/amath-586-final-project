import numpy as np

class CrankNicholsonSolver:
    '''
    Solves the heat equation with von Neumann boundary conditions
    '''

    def __init__(self, initial_state, left_flux, right_flux, timestep, grid_size,
                 start_grid=0, end_grid=1, start_time=0, end_time=1, max_iters=1000):
        self.initial_state = initial_state
        self.left_flux = left_flux
        self.right_flux = right_flux
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
        h = (xf - x0) / (m + 1)
        max_iters = self.max_iters
        t = t0
        u = np.concatenate(([1], self.initial_state))
        grid_points = np.linspace(x0, xf, m+2, endpoint=True)
        yield t, u[1:]
        iters += 1
        r = k / (2 * np.power(h, 2))
        #print(h, k, r)
        A = np.diagflat((m+2) * [-2]) + np.diagflat((m+1) * [1], k=-1) + np.diagflat((m+1) * [1], k=1)
        identity = np.identity(m+2)
        A1 = np.zeros((m+2, m+2))
        A1[0, :3] = [3., -4., 1.]
        A1[-1, -3:] = [-3 + 2 * self.right_flux * h, 4, -1]
        A1[1:-1, :] = (identity - r * A)[1:-1, :]
        #print(np.array_str(A1, precision=2))
        A2 = np.zeros((m+2, m+3))
        A2[1:-1, 1:] = (identity + r * A)[1:-1, :]
        A2[0,0] = 2 * self.left_flux * h
        A2[-1, 0] = 2 * self.right_flux * h
        #print(np.array_str(A2, precision=2))
        while t < tf and iters <= max_iters:
            t_old = t
            t = t0 + k * iters
            rhs = np.matmul(A2, u)
            u[1:] = np.linalg.solve(A1, rhs)
            yield t, u[1:]
            iters += 1

    __iter__ = step

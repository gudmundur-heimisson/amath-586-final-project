import numpy as np
import ode

a = np.array([[1,2,5],[3,4,6]])
print(a.shape)
shape = ode.get_shape(a)
print(shape)
print(type(shape))

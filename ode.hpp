#ifndef ODE_H
#define ODE_H

#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <iostream>

namespace py = boost::python;
namespace np = boost::python::numpy;

class ForwardEulerSolver {
    public:
        double initial_value, step_size, start_location, end_location;
        int max_iters;
        ForwardEulerSolver (double initial_value, 
                            double step_size, 
                            double start_location = 0,
                            double end_location = -1,
                            int max_iters = -1 ): 
            initial_value(initial_value),
            step_size(step_size),
            start_location(start_location),
            end_location(end_location),
            max_iters(max_iters) {}
};

#endif
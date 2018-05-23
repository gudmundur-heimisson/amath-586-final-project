#ifndef ODE_H
#define ODE_H

#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <iostream>

namespace py = boost::python;
namespace np = boost::python::numpy;

py::tuple getShape(np::ndarray a) {
    std::cout << "In getShape" << std::endl;
    py::tuple shape = py::extract<py::tuple>(a.attr("shape"));
    return shape;
}

#endif
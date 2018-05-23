#include "ode.hpp"
#include <Python.h>
#include <boost/python.hpp>

namespace py = boost::python;
namespace np = boost::python::numpy;

BOOST_PYTHON_MODULE(ode) {
    np::initialize();
    py::class_<ForwardEulerSolver>("ForwardEulerSolver", py::init<double, double, double, double, int>());
}

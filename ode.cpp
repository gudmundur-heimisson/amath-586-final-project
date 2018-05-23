#include "ode.hpp"
#include <Python.h>
#include <boost/python.hpp>

namespace py = boost::python;
namespace np = boost::python::numpy;

BOOST_PYTHON_MODULE(ode) {
//   Py_Initialize();
    np::initialize();
    py::def("get_shape", getShape);
}

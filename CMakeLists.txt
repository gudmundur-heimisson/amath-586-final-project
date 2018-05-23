project (PyODE)
cmake_minimum_required(VERSION 2.8)

find_package(PythonLibs 3.5)
include_directories (${PYTHON_INCLUDE_DIRS})

find_package(Boost 1.67 COMPONENTS python35 numpy35)
include_directories (${Boost_INCLUDE_DIRS})

#include_directories (${numpy_INCLUDE_DIR})

add_library(
  ode SHARED
  ode.cpp
)

set_target_properties(
  ode
  PROPERTIES PREFIX ""
)

target_link_libraries (
  ode
  ${PYTHON_LIBRARIES}
  ${Boost_LIBRARIES}
)

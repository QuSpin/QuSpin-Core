#pragma once

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <quspin/array/array.hpp>

namespace py = pybind11;

quspin::DType numpy_to_quspin_dtype(const py::dtype &);
quspin::Array to_array(py::buffer &);
const quspin::Array to_array(const py::buffer &);

void define_array(py::module_ &);

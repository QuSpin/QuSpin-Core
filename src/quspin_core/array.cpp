#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(array, m) {
  m.doc() = "Python binding for quspin arrays";
  m.def("hello", []() { return "Hello, World!"; });
}

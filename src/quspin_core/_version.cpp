#include <pybind11/pybind11.h>
#include <quspin/array/array.hpp>

#define QUOTE(name) #name
#define STR(macro) QUOTE(macro)

#define VERSION_STR STR(VERSION_INFO)

namespace py = pybind11;

PYBIND11_MODULE(_version, m) {
  m.def("_get_version", []() { return VERSION_STR; });
}

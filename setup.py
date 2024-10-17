# Available at setup time due to pyproject.toml
import glob
import subprocess
import os
import sys
from typing import Dict, List
from pybind11.setup_helpers import Pybind11Extension, build_ext, ParallelCompile
from setuptools import setup

# Optional multithreaded build
ParallelCompile("NPY_NUM_BUILD_JOBS").install()


__version__ = "0.1.0"

CWD = os.path.dirname(os.path.abspath(__file__))
LIBQUISPIN_BUILD_DIR = os.path.join(CWD, "libquspin-build")
LIBQUSPIN_DIR = os.path.join(CWD, "libquspin")


def extra_compile_args() -> List[str]:
    if sys.platform == "win32":
        extra_compile_args = ["/openmp", "/std:c++20"]
    elif sys.platform in ["darwin"]:
        extra_compile_args = [
            "-DLLVM_ENABLE_PROJECTS",
            "-Xpreprocessor",
            "-fopenmp-version=50",
            "-fopenmp",
            "--std=c++20",
        ]
    else:
        extra_compile_args = ["-fopenmp", "-std=c++2a"]

    if os.environ.get("COVERAGE", False):
        if sys.platform in ["win32", "cygwin", "win64", "darwin"]:
            raise ValueError("Coverage is not supported on Windows or macOS")

        extra_compile_args += [
            "--coverage",
            "-fno-inline",
            "-fno-inline-small-functions",
            "-fno-default-inline",
            "-O0",
        ]

    return extra_compile_args


def extra_link_args() -> List[str]:
    if sys.platform in ["win32", "cygwin", "win64"]:
        extra_link_args = ["/openmp"]
    elif sys.platform in ["darwin"]:
        extra_link_args = [
            "-DLLVM_ENABLE_PROJECTS",
            "-Xpreprocessor",
            "-fopenmp-version=50",
            "-fopenmp",
        ]
    else:
        extra_link_args = ["-fopenmp"]

    if os.environ.get("COVERAGE", False):
        if sys.platform in ["win32", "cygwin", "win64", "darwin"]:
            raise ValueError("Coverage is not supported on Windows or macOS")

        extra_link_args += ["--coverage"]

    return extra_link_args


def setup_quspin_core() -> Dict[str, List[str]]:
    def run_cmd(cmds: list[str]):
        res = subprocess.run(cmds, stdout=sys.stdout, stderr=sys.stderr, cwd=CWD)

        if res.returncode == 0:
            return

        raise RuntimeError("Failed to build libquspin")

    if sys.platform == "win32":
        obj_ext = "obj"
        lib_file = "quspin.lib"
    elif sys.platform == "darwin":
        obj_ext = "o"
        lib_file = "libquspin.dylib"
    elif sys.platform == "linux":
        obj_ext = "o"
        lib_file = "libquspin.so"
    else:
        raise ValueError(f"Unsupported platform {sys.platform}")

    run_cmd(
        [
            "meson",
            "setup",
            "libquspin",
            LIBQUISPIN_BUILD_DIR,
            "--reconfigure",
            "--buildtype=release",
        ]
    )
    run_cmd(["meson", "test", "-C", LIBQUISPIN_BUILD_DIR, "-j4"])

    files_glob = os.path.join(LIBQUISPIN_BUILD_DIR, f"{lib_file}.p")
    extra_objects = glob.glob(os.path.join(files_glob, f"*.{obj_ext}"))

    if len(extra_objects) == 0:
        os.listdir(files_glob)
        raise RuntimeError(f"No object files found in {files_glob}")

    include_dirs = [os.path.join(LIBQUSPIN_DIR, "include")]

    bindings_cpp = os.path.join("src", "quspin_core", "_bindings.cpp")
    submodules_cpp = glob.glob(
        os.path.join("src", "quspin_core", "_submodules", "*.cpp")
    )

    include_dirs.append(os.path.join("src", "quspin_core"))

    return Pybind11Extension(
        "quspin_core._bindings",
        sorted([bindings_cpp, *submodules_cpp]),
        extra_objects=extra_objects,
        extra_compile_args=extra_compile_args(),
        extra_link_args=extra_link_args(),
        include_dirs=include_dirs,
        define_macros=[("VERSION_INFO", __version__)],
    )


setup(
    ext_modules=[setup_quspin_core()],
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)

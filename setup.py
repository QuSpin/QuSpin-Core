# Available at setup time due to pyproject.toml
import glob
import locale
import shutil
import subprocess
import os
import sys
from typing import Dict, List
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup


__version__ = "0.1.0"

LIB_QUISPIN_BUILD = False
LIBQUISPIN_BUILD_DIR = "libquspin-build"
LIBQUSPIN_DIR = "libquspin"


def extra_compile_args() -> List[str]:
    if sys.platform in ["win32", "cygwin", "win64"]:
        extra_compile_args = ["/openmp", "/std:c++20"]
    if sys.platform in ["darwin"]:
        extra_compile_args = [
            "-DLLVM_ENABLE_PROJECTS",
            "-Xpreprocessor",
            "-fopenmp-version=50" "-fopenmp",
            "--std=c++20",
        ]
    else:
        extra_compile_args = ["-fopenmp", "--std=c++20"]

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
    if sys.platform in ["darwin"]:
        extra_link_args = [
            "-DLLVM_ENABLE_PROJECTS",
            "-Xpreprocessor",
            "-fopenmp-version=50" "-fopenmp",
        ]
    else:
        extra_link_args = ["-fopenmp"]

    if os.environ.get("COVERAGE", False):
        if sys.platform in ["win32", "cygwin", "win64", "darwin"]:
            raise ValueError("Coverage is not supported on Windows or macOS")

        extra_link_args += ["--coverage"]

    return extra_link_args


def build_libquspin() -> Dict[str, List[str]]:
    def check(res: subprocess.CompletedProcess[bytes]):
        if res.returncode == 0:
            return

        strerr = res.stdout.decode(
            "utf-8" if sys.flags.utf8_mode else locale.getencoding()
        )
        raise RuntimeError(f"Failed to build libquspin: {strerr}")

    check(
        subprocess.run(
            ["meson", "setup", "libquspin", LIBQUISPIN_BUILD_DIR, "--reconfigure"],
        )
    )

    check(
        subprocess.run(
            ["meson", "compile", "-C", LIBQUISPIN_BUILD_DIR, "-j", "4"],
        )
    )

    relocatation_dir = os.path.join("src", "quspin_core", "lib")
    if not os.path.exists(relocatation_dir):
        os.mkdir(relocatation_dir)

    for lib_file in [
        "libquspin.so",
        "libquspin.dylib",
        "libquspin.dll",
        "libquspin.lib",
    ]:
        if os.path.exists(os.path.join(LIBQUISPIN_BUILD_DIR, lib_file)):
            shutil.copy(
                os.path.join(LIBQUISPIN_BUILD_DIR, lib_file),
                os.path.join(relocatation_dir, lib_file),
            )
            break

    shutil.copytree(
        os.path.join(LIBQUSPIN_DIR, "include"),
        os.path.join("src", "quspin_core", "include"),
        dirs_exist_ok=True,
    )

    libraries = ["quspin"]
    library_dirs = [os.path.join("src", "quspin_core", "lib")]
    runtime_library_dirs = library_dirs if sys.platform != "win32" else None
    include_dirs = [os.path.join("src", "quspin_core", "include")]

    return {
        "libraries": libraries,
        "library_dirs": library_dirs,
        "runtime_library_dirs": runtime_library_dirs,
        "include_dirs": include_dirs,
        "extra_link_args": ["-Wl,-rpath=$ORIGIN/lib"],
    }


def find_extensions(**ext_options) -> List[Pybind11Extension]:
    extensions = []
    for filename in glob.glob("src/quspin_core/*.cpp"):
        name = os.path.splitext(os.path.basename(filename))[0]
        ext = Pybind11Extension(f"quspin_core.{name}", [filename], **ext_options)
        extensions.append(ext)

    return extensions


ext_options = build_libquspin()
ext_options["extra_compile_args"] = (
    ext_options.get("extra_compile_args", []) + extra_compile_args()
)
ext_options["extra_link_args"] = (
    ext_options.get("extra_link_args", []) + extra_link_args()
)
ext_options["define_macros"] = [("VERSION_INFO", __version__)]

setup(
    ext_modules=find_extensions(**ext_options),
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    packages=["quspin_core"],
    package_dir={"quspin_core": "src/quspin_core"},
    package_data={"quspin_core": ["lib/*", "include/**/*.hpp"]},
)

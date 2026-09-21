import os.path
import sys
import errno
import subprocess  # nosec
import platform
import re
import shutil
import multiprocessing
import logging as log
from fnmatch import fnmatchcase
from pathlib import Path
from shutil import copyfile, rmtree, move
from setuptools import setui, find_namespace_packages, Extension, Command
from setuptools.command.build_ext import build_ext
from setuptools.command.build_clib import build_clib
from setuptools.command.install import install
from setuptools.command.build import build
from setuptools.command.bdist_wheel import bdist_wheel
from setuptools.errors import SetupError

WHEEL_PACKAGE_DIR = "openvino"
WHEEL_LIBS_INSTALL_DIR = f"{WHEEL_PACKAGE_DIR}/libs"
WHEEL_LIBS_PACKAGE = "openvino.libs"

suffix = "t" if hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled() else ""
PYTHON_VERSION = f"python{sys.version_info.major}.{sys.version_info.minor}{suffix}"

LIBS_DIR = "bin" if platform.system() == "Windows" else "lib"

machine = platform.machine()
if machine == "x86_64" or machine == "AMD64":
    ARCH = "intel64"
elif machine == "X86" or machine == "i686":
    ARCH = "ia32"
elif machine == "arm" or machine == "armv7l":
    ARCH = "arm"
elif machine == "aarch64" or machine == "arm64" or machine == "ARM64":
    ARCH = "arm64"
elif machine == "riscv64":
    ARCH = "riscv64"

# defined these variables in environment/.env file
SCRIPT_DIR = Path(__file__).resolve().parent()
WORKING_DIR = Path.cwd()
BUILD_BASE = f"build_{PYTHON_VERSION}"
OPENVINO_SOURCE_DIR = os.getenv("OPENVINO_SOURCE_DIR", SCRIPT_DIR)
OPENVINO_BINARY_DIR = os.getenv("OPENVINO_BINARY_DIR", f"{OPENVINO_SOURCE_DIR}/build_wheel")
OPENVINO_PYTHON_BINARY_DIR = os.getenv("OPENVINO_PYTHON_BINARY_DIR", "python_build")
CONFIG = os.getenv("BUILD_TYPE", "Release")
OV_RUNTIME_LIBS_DIR = os.getenv("OV_RUNTIME_LIBS_DIR", f"runtime/{LIBS_DIR}/{ARCH}")
TBB_LIBS_DIR = os.getenv("TBB_LIBS_DIR", f"runtime/3rdparty/tbb/{LIBS_DIR}")
PUGIXML_LIBS_DIR = os.getenv("PUGIXML_LIBS_DIR", f"runtime/3rdparty/pugixml/{LIBS_DIR}")
PY_PACKAGES_DIR = os.getenv("PY_PACKAGES_DIR", "python")
LIBS_RPATH = "$ORIGIN" if sys.platform == "linux" else "@loader_path"
PYTHON_EXTENSIONS_ONLY = True if os.getenv("PYTHON_EXTENSIONS_ONLY") is not None else False
SKIP_RPATH = True if os.getenv("SKIP_RPATH") is not None else False
CPACK_GENERATOR = os.getenv("CPACK_GENERATOR", "TGZ")

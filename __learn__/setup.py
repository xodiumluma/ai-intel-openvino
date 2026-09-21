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

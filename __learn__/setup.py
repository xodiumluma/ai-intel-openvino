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

WHEEL_PACKAGE_DIR = "openvino"
WHEEL_LIBS_INSTALL_DIR = f"{WHEEL_PACKAGE_DIR}/libs"

"pi-top Python Common Library"

import os
import sys
from setuptools import setup, find_packages

if sys.version_info[0] == 3:
    if not sys.version_info >= (3, 2):
        raise ValueError("This package requires Python 3.2 or above")
else:
    raise ValueError("Unrecognized major version of Python")

HERE = os.path.abspath(os.path.dirname(__file__))

# Workaround <http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html>
try:
    import multiprocessing  # noqa: F401
except ImportError:
    pass

with open(os.path.join(HERE, "debian/rules")) as search:
    for line in search:
        if "export PYBUILD_NAME=" in line:
            __project__ = line.split("=")[1].rstrip()
            break

assert __project__ != ""

# Get first field of the changelog
with open(os.path.join(HERE, "debian/changelog")) as f:
    first_line_changelog = f.readline()

# Get Debian version from first field; strip surrounding brackets
debian_version = first_line_changelog.split(" ")[1].rstrip()[1:-1]

# Convert Debian version to Python version
python_version = debian_version
for r in (
    ("(", ""),
    (")", ""),

    # Convert from gbp version format to PEP 440 local version format:
    # (replace '~' with '+')
    # See https://www.python.org/dev/peps/pep-0440/#local-version-identifiers for more information
    ("~", "+"),

    # Convert from Debian epoch version format to PEP 440 epoch version format:
    # (replace ':'' with '!')
    # See https://www.python.org/dev/peps/pep-0440/#version-epochs for more information
    (":", "!"),
):
    python_version = python_version.replace(*r)

__version__ = python_version
assert __version__ != ""

project = "pi-top Python Common Library"
__author__ = "pi-top"
__author_email__ = "deb-maintainers@pi-top.com"

__url__ = "https://github.com/pi-top/pi-top-Python-Common-Library"
__platforms__ = "ALL"

# https://pypi.org/classifiers/
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: System :: Hardware",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: PyPy",
]

__keywords__ = [
    "pi-top",
    "raspberrypi",
]

__requires__ = [
    # For reviewing DHCP leases
    "isc_dhcp_leases",
    # For network interface checking
    "netifaces",
    # For journal logging
    "python-systemd",
]

__extra_requires__ = {
    "doc":   ["sphinx"],
    "test":  ["pytest", "coverage", "mock", "parameterized"],
}

if sys.version_info[:2] == (3, 2):
    # Particular versions are required for Python 3.2 compatibility
    __extra_requires__["doc"].extend([
        "Jinja2<2.7",
        "MarkupSafe<0.16",
    ])
    __extra_requires__["test"][0] = "pytest<3.0dev"
    __extra_requires__["test"][1] = "coverage<4.0dev"
elif sys.version_info[:2] == (3, 3):
    __extra_requires__["test"][0] = "pytest<3.3dev"
elif sys.version_info[:2] == (3, 4):
    __extra_requires__["test"][0] = "pytest<5.0dev"

__entry_points__ = {
}


def main():
    import io
    with io.open(os.path.join(HERE, "README.rst"), "r") as readme:
        setup(
            name=__project__,
            version=__version__,
            description=__doc__,
            long_description=readme.read(),
            classifiers=__classifiers__,
            author=__author__,
            author_email=__author_email__,
            url=__url__,
            license=[
                c.rsplit("::", 1)[1].strip()
                for c in __classifiers__
                if c.startswith("License ::")
            ][0],
            keywords=__keywords__,
            packages=find_packages(),
            include_package_data=True,
            platforms=__platforms__,
            install_requires=__requires__,
            extras_require=__extra_requires__,
            entry_points=__entry_points__,
        )


if __name__ == "__main__":
    main()

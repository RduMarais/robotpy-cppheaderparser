#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from os.path import dirname, exists, join
import sys, subprocess

from setuptools import find_packages, setup

setup_dir = dirname(__file__)
git_dir = join(setup_dir, ".git")
version_file = join(setup_dir, "CppHeaderParser", "version.py")

# Automatically generate a version.py based on the git version
if exists(git_dir):
    p = subprocess.Popen(
        ["git", "describe", "--tags", "--long", "--dirty=-dirty"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = p.communicate()
    # Make sure the git version has at least one tag
    if err:
        print("Error: You need to create a tag for this repo to use the builder")
        sys.exit(1)

    # Convert git version to PEP440 compliant version
    # - Older versions of pip choke on local identifiers, so we can't include the git commit
    v, commits, local = out.decode("utf-8").rstrip().split("-", 2)
    if commits != "0" or "-dirty" in local:
        v = "%s.post0.dev%s" % (v, commits)

    # Create the version.py file
    with open(version_file, "w") as fp:
        fp.write("# Autogenerated by setup.py\n__version__ = '{0}'".format(v))

with open(version_file, "r") as fp:
    exec(fp.read(), globals())

DESCRIPTION = (
    "Parse C++ header files and generate a data structure " "representing the class"
)


CLASSIFIERS = [
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: C++",
    "License :: OSI Approved :: BSD License",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Disassemblers",
]

setup(
    name="robotpy-cppheaderparser",
    version=__version__,
    author="Jashua Cloutier",
    author_email="jashuac@bellsouth.net",
    maintainer="RobotPy Development Team",
    maintainer_email="robotpy@googlegroups.com",
    url="https://github.com/robotpy/robotpy-cppheaderparser",
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    license="BSD",
    platforms="Platform Independent",
    packages=["CppHeaderParser"],
    keywords="c++ header parser ply",
    classifiers=CLASSIFIERS,
    requires=["ply"],
    install_requires=["ply"],
    package_data={
        "CppHeaderParser": ["README", "README.html", "doc/*.*", "examples/*.*"]
    },
)

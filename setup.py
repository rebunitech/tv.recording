import pathlib
import re

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent


def get_discription():
    """
    Read full description from `README.md`
    """

    with open("README.md", "r") as long_description:
        return long_description.read()


def get_version():
    """
    Read version
    """
    txt = (WORK_DIR / "tv_recording" / "__init__.py").read_text("utf-8")
    try:
        return re.findall(
            r"^__version__\s+=\s+['|\"]([^']+)['|\"]\r?$", txt, re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


setup(
    name="amerti",
    version=get_version(),
    author="Wendirad Demelash",
    author_email="wendiradame@gmail.com",
    description="TV Station Media Recorder",
    long_description=get_discription(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "tests.*", "examples.*", "docs")),
    url="https://github.com/rebunitech/tv.recording",
    license="Apache License 2.0",
    python_requires=">=3.10",
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "tv-record = tv_recording.__main__:main",
        ],
    },
)

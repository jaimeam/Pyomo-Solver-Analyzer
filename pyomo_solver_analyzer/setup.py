from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyomo-solver-analyzer",
    version="0.1.0",
    author="Pyomo Solver Analyzer Contributors",
    description="Automatic constraint analysis and debugging for Pyomo linear solvers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyomo-solver-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyomo>=6.0",
    ],
)

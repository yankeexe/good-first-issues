"""Package setup"""
import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

requirements = ["halo", "requests", "click", "tabulate", "rich<=7.1.0"]

# Development Requirements
requirements_dev = ["pytest<=4.*", "black<=20.8b1", "pre-commit", "mypy"]

setuptools.setup(
    name="good-first-issues",
    version="2.0.0",
    author="Yankee Maharjan",
    author_email="yankee.exe@gmail.com",
    url="https://github.com/yankeexe/good-first-issues",
    description="Find good first issues right from your CLI!",
    license="MIT",
    packages=setuptools.find_packages(exclude=["dist", "build", "*.egg-info"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    entry_points={"console_scripts": ["gfi = good_first_issues.main:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
)

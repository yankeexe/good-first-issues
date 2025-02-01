"""Package setup"""

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

requirements = [
    "halo==0.0.31",
    "requests==2.32.3",
    "click==8.1.7",
    "tabulate==0.9.0",
    "rich<=13.7.1",
]
requirements_dev = ["pytest==8.2.2", "ruff==0.9.4", "pre-commit", "mypy"]

setuptools.setup(
    name="good-first-issues",
    version="2.1.4",
    author="Yankee Maharjan",
    url="https://github.com/yankeexe/good-first-issues",
    description="Find good first issues right from your CLI!",
    license="MIT",
    packages=setuptools.find_packages(exclude=["dist", "build", "*.egg-info"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    entry_points={"console_scripts": ["gfi = good_first_issues.main:cli"]},
    python_requires=">=3.9",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yankeexe/good-first-issues/issues",
        "Source": "https://github.com/yankeexe/good-first-issues",
    },
)

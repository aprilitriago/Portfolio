from setuptools import setup, find_packages

setup(
    name="liquidh2o",
    version="0.1.0",
    description="Water tank analytics & forecasting pipeline (time-aware LightGBM).",
    packages=find_packages(exclude=("tests", "notebooks")),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[],
)

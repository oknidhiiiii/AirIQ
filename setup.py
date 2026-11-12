from setuptools import setup, find_packages

setup(
    name="airiq",
    version="0.1.0",
    description="Airbnb Pricing & Market Intelligence Using Apache PySpark",
    author="Antigravity Team",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "airiq = airiq.cli:main",
        ],
    },
)

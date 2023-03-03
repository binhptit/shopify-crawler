from setuptools import setup, find_packages

# read the contents of the requirements.txt file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Shopify Crawler",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "dev": [
            "pre-commit",
            "pytest",
        ]
    }
)
from setuptools import setup, find_packages

pkg_name = "snakifyer"


def read_file(fname):
    with open(fname, "r") as f:
        return f.read()


requirements = [
    "beautifulsoup4",
    "requests",
    "rich",
]

setup(
    name=pkg_name,
    version="1.0.2",
    author="Akash R Chandran",
    author_email="chandranrakash@gmail.com",
    description="A simple to bot to automate problem submissions on snakify.org ",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/akashrchandran/snakifyer",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "snakifyer = snakifyer:main",
        ],
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

# rm -f dist/*
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
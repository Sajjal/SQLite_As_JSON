from setuptools import setup, find_packages
import os

current_dir = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open(os.path.join(current_dir, "README.md"), encoding="utf-8") as readme:
        return "\n" + readme.read()


VERSION = '1.0.1'
DESCRIPTION = 'Do SQLite CRUD operation via JSON object'
LONG_DESCRIPTION = readme()

# Setting up
setup(
    name="SQLiteAsJSON",
    version=VERSION,
    author="Sajjal Neupane (https://mrsajjal.com)",
    url="https://github.com/Sajjal/SQLite_As_JSON",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['sqlite as json', 'sql json', 'sqlite orm', 'sqlite nosql', 'sqlite json', 'json sqlite'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

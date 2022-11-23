import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tppscheduling",
    version="1.0.0",
    author="André L. Maravilha",
    author_email="andre.maravilha@outlook.com",
    description="Scheduling term paper presentations through optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andremaravilha/tpp-scheduling",
    packages=setuptools.find_packages(),
    requires=["gurobipy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
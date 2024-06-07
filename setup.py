from setuptools import setup, find_packages

setup(
    name="loop-controller",
    version="0.1.1",
    author="Marcos Edo Atienza",
    author_email="topermaper@gmail.com",
    description="Loop controllers for managing execution intervals",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/topermaper/loop-controller.git",
    packages=find_packages(),
    py_modules=["pidloopcontroller", "meanloopcontroller"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
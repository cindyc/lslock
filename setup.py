from setuptools import setup

setup(
        name="lslock",
        version="0.1.0",
        description="Prints locked files under a directory",
        author="Cindy Cao",
        author_email="cindy.hy.cao@gmail.com",
        url="http://github.com/cindyc/lslock",
        packages=["lslock"],
        install_requires=["pytest"],
)

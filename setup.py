from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'lslock = lslock:main',
        ],
    },
    name="lslock",
    version="0.1.0",
    description="lslock: list locked files under a directory",
    author_email="cindy.hy.cao@gmail.com",
    url="http://github.com/cindyc/lslock",
    install_requires=["prettytable"],
    tests_require=["pytest"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],
    packages=["lslock"],
)

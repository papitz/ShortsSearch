from setuptools import setup

setup(
    name='short_search',
    version='0.1.0',
    py_modules=['short_search'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'short_search = short_search:cli',
        ],
    },
)

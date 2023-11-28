from setuptools import setup, find_packages

setup(
    name='short_search',
    version='0.1.0',
    py_modules=['short_search'],
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'short_search = short_search:cli',
        ],
    },
)

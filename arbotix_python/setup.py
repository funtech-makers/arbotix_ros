#!/usr/bin/env python3


"""Asterix metapackage."""


from os import path
from glob import glob
from setuptools import setup, find_packages


package_name = 'arbotix_python'


setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(),
    data_files=[
        (path.join('share', package_name), ['package.xml']),
        (path.join('share', package_name, 'params'), glob('params/*')),
    ],
    zip_safe=True,
    install_requires=['setuptools'],
    author='Ewen BRUN',
    author_email='ewen.brun@ecam.fr',
    maintainer='Ewen BRUN',
    maintainer_email='ewen.brun@ecam.fr',
    keywords=['ROS2', '', 'CDFR'],
    description='Asterix RO2 System',
    license='Funtech Makers :: CDFR 2020',
    entry_points={
        'console_scripts': [
            'arbotix_gui = arbotix_python.arbotix_gui:main',
            'arbotix_driver = arbotix_python.arbotix_driver:main',
            'arbotix_terminal = arbotix_python.arbotix_terminal:main',
        ],
    },
)

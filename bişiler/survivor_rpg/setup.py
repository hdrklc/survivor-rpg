#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Survivor RPG
"""

from setuptools import setup, find_packages

setup(
    name="survivor-rpg",
    version="1.0.0",
    description="Professional Survivor RPG Game",
    author="Game Developer",
    packages=find_packages(),
    install_requires=[
        "kivy>=2.1.0",
        "kivymd>=1.0.0"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'survivor-rpg=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Arcade",
    ],
)


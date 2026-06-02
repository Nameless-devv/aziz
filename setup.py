#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qishloq xo'jaligi roboti - Setup Script
Setup skripti proyektni global buyruq sifatida o'rnatish uchun
"""

from setuptools import setup, find_packages
from pathlib import Path

# README faylni o'qish
here = Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8") if (here / "README.md").exists() else ""

setup(
    name="aziz-robo",
    version="1.0.0",
    description="Qishloq xo'jaligi roboti - Coverage Path Planning tizimi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    python_requires=">=3.8",
    
    # Paketlar va modullar
    packages=find_packages(where="."),
    py_modules=["robo"],
    include_package_data=True,
    
    # Asosiy zависимости
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "pygame>=2.1.0",
        "pillow>=8.0.0",
        "pandas>=1.3.0",
        "shapely>=1.8.0",
        "pyyaml>=5.4.0",
        "pytest>=6.0.0",
    ],
    
    # Entry points - bu "aziz" buyrug'ini yaratadi
    entry_points={
        "console_scripts": [
            "aziz=robo:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    # Fayllar
    data_files=[
        ("config", ["config/settings.yaml"]),
    ],
)

# -*- coding: utf-8 -*-

from setuptools import setup

# def readme():
#     with open("README.md") as f:
#         return f.read()

setup(name="drawBotGrid",
      version="0.1.2",
      description="a little helper for grid based layout in DrawBot",
      long_description="TBD",
      classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Build Tools",
      ],
      author="Mathieu Reguer",
      author_email="mathieu.reguer@gmail.com",
      license="All rights reserved",
      packages=[
        "drawBotGrid",
        ],
      install_requires=[
        #"drawBot",

      ],
      include_package_data=True,
      zip_safe=False)

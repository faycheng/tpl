# -*- coding:utf-8 -*-

from setuptools import find_packages, setup

README = """# tpl
"""


setup(
    name='tpl',
    version='0.1.0',
    description='Command line utility for generating files or directories from template',
    long_description=README,
    author='程飞',
    url='https://github.com/faycheng/tpl.git',
    packages=find_packages(exclude=['tests']),
    install_requires=['prompt_toolkit==1.0.15', 'six==1.10.0', 'pytest==3.2.1', 'Jinja2==2.9.6', 'click==6.7', 'delegator.py==0.0.13', 'delegator==0.0.3'],
    entry_points={
        'console_scripts': ['tpl=cli:tpl'],
    },
    py_modules=['cli'],
    zip_safe=True,
    license='MIT License',
    classifiers=['development status :: 1 - planning', 'topic :: utilities', 'intended audience :: developers', 'programming language :: python :: 3 :: only', 'environment :: macos x']
)
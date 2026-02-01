'''
This setup.py file is an  essential part of packaging and distributing Python projects.
It is used by setuptools (or distutils in older Pyhton versions) to define the configuration
of ypur project, such as its metadata, dependencies and more.
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    '''    
    This function will return list of requirements
    :rtype: List[str]
    '''
    lst_requirement : List[str] = []
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()    #Read lines from requirements.txt

            for line in lines:
                requirement = line.strip()
                # We need to ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    lst_requirement.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return lst_requirement

setup(
    name = "Network Security",
    author= "Alok",
    author_email="alok@gmail.com",
    version="0.0.1",
    packages= find_packages(),
    install_requires = get_requirements()
)
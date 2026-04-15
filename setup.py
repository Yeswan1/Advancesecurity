
from setuptools import setup,find_packages
from typing import List
requirement_setup:list[str]=[]
def find_pack():
    try:
       with open('requirements.txt','rb') as file:
           lines=file.readlines()
           for line in lines:
                requirements=line.strip()
                if requirements and requirements!='-e .':
                    requirement_setup.append(requirements)

    except FileNotFoundError:
        print('File not found error')

        return requirement_setup
    

setup(
    name='Security',
    version='0.0.1',
    author='Yeswanth',
    author_email='yeswanthsuryaraj02@gmail.com',
    packages=find_packages(),
    install_requires=find_pack()
)
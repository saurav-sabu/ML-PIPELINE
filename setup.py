# Import necessary modules
from setuptools import setup,find_packages
from typing import List

# Define a constant for a specific requirement string
HYPHEN_E_DOT = "-e ."

# Define a function to read and clean requirements from a file
def get_requirements(filepath:str) -> List[str]:
    
    requirements = []

    # Open the specified file
    with open(filepath) as file_obj:
        
        # Read lines and remove newline characters
        requirements = file_obj.readlines()
        requirements = [x.replace("\n","") for x in requirements]

        # Check for and remove the specific requirement string
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

# Configure the package information for setuptools
setup(name="ML_Pipeline_Project",
      version="0.0.1",
      description="Machine Learning Pipeline Project",
      author="Saurav Sabu",
      author_email="saurav.sabu9@gmail.com",
      packages=find_packages(),
      install_requires = get_requirements("requirements.txt"))



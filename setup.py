from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import numpy as np
import os,sys

def pwd():
    return os.path.split(os.path.abspath(__file__))[0]

def get_includes():
    return [np.get_include(),os.path.join(pwd(),"src","includes")]
    
def get_library_dirs():
    return [os.path.join(pwd(),"src","quspin_abi")]

if __name__ == "__main__":

    with open("README.md", 'r') as f:
        long_description = f.read()
        
    ext = [
        Extension("src.quspin_api.basis", [os.path.join(pwd(),"src","quspin_api","basis.pyx")],
            include_dirs=get_includes(),
            language_level=3,
            language="c++",
        ),
        Extension("src.quspin_api.operators", [os.path.join(pwd(),"src","quspin_api","operator.pyx")],
            include_dirs=get_includes(),
            language_level=3,
            language="c++",
        ),
    ]
    
    setup(
        name="QuSpin-Core",
        version="0.0.1a0",
        zip_safe=False,
        packages=find_packages(where="src/quspin_api"),
        author="Phillip Weinberg, Marin Bukov, Markus Schmitt",
        description="Base low-level components for QuSpin.",
        long_description=long_description,
        long_description_content_type='text/markdown',
        url="https://github.com/weinbe58/QuSpin-C-API",
        ext_modules=cythonize(ext),
                install_requires=[
            'numpy>=1.19.2'
        ],
        include_dirs=get_includes(),
    )
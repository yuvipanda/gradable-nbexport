from setuptools import setup, find_packages

setup(
    name="gradable_nbexport",
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'nbconvert',
        'ipython'
    ]
)

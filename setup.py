from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='defi-playground',
    version='0.0.1',
    description='A simple getting started testchain for DeFi protocol development',
    long_description=long_description,    
    license='MIT',
    author='Dominik Harz',
    author_email='dominik.harz@gmail.com',
    packages=['playground'],
    entry_points={
        'console_scripts': [
            'playground = playground.__main__:main'
        ]
    },
)

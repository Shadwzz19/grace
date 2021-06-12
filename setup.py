from setuptools import *


setup(
    name='Grace',
    description='The Code Society community Bot',
    version='0.0.0',
    author='Code Society Lab',
    author_email='',
    python_require='>=3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'coloredlogs',
        'logger',
        'python-dotenv',
        'discord',
        'emoji',
        'nltk',
    ],
)

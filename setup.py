from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name = "Anime_Recommender_MLOPS",
    version= "0.1",
    author= "Sawan",
    packages = find_packages(),
    install_requires= requirements,

)
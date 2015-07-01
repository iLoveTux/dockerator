from setuptools import setup, find_packages
setup(
    name = "dockerator",
    version = "0.6.0",
    packages = find_packages(),

    install_requires = ['docker-py'],

    author = "iLoveTux",
    author_email = "me@ilovetux.com",
    description = "Provides a decorator which can pull and spin up a docker container and ensure that it is running before executing the function.",
    license = "GPLv2",
    keywords = "docker docker-py decorator images containers",
    url = "http://github.com/ilovetux/dockerator",   # project home page, if any

)

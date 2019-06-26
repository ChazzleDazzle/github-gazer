from setuptools import setup

setup(
    name='gazer',
    version='0.1',
    description='Watch for GitHub review requests, and release branch pull requests, and notify on Slack.',
    author='Charlie Gibson',
    author_email='gibson@csdisco.com',
    packages=['gazer'],
    license="MIT",
    install_requires=[
        "PyGithub",
        "PyYAML",
        "requests",
    ],
    zip_safe=False, 
    scripts=["bin/gazer"],
)

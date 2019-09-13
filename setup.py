from setuptools import setup

setup(
    name="gazer",
    version="0.0.3",
    description="Watch GitHub for my review requests, or pull requests to release branches, and notify over Slack.",
    author="Charlie Gibson",
    author_email="gibson.charlie@gmail.com",
    packages=["gazer"],
    license="MIT",
    install_requires=["PyGithub", "PyYAML", "requests"],
    zip_safe=False,
    scripts=["bin/gazer"],
)

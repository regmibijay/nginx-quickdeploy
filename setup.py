import json
import os

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open(os.path.join(os.path.dirname(__file__), "nginx_quickdeploy", "version.json"), "r") as f:
    version = json.loads(f.read())

setuptools.setup(
    name="nginx_quickdeploy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version["version"],
    packages=setuptools.find_packages(),
    data_files=[("nginx_quickdeploy", ["nginx_quickdeploy/version.json"])],
    include_package_data=True,
    url="https://github.com/regmibijay/nginx-quickdeploy",
    license="MIT",
    author="Bijay Regmi",
    author_email="github@regdelivery.de",
    description="Nginx Quickdeploy",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "quickdeploy=nginx_quickdeploy.main:main",
        ]
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

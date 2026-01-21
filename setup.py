from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sbc_cr34/__init__.py
from sbc_cr34 import __version__ as version

setup(
    name="sbc_cr34",
    version=version,
    description="Sistema de Gestión de Clientes Turísticos - SBC CRM",
    author="SBC Internationals",
    author_email="sbcinternational@protonmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)

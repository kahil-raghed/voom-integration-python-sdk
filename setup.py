from setuptools import setup, find_packages

setup(
    name="voom-integration-sdk",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Voom",
    description="Python SDK for Voom CRM Integration",
    python_requires=">=3.7",
)

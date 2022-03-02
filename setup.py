
"""Basic package information."""
from setuptools import setup, find_packages

install_requires = [
    'lemur',
    'boto3',
]

setup(
    name='lemur-cloudwatch',
    version='1.0.0',
    author='Nicolas Surleraux',
    author_email='nicolas.surlerauxe@railnova.eu',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    license='MIT',
    entry_points={
        'lemur.plugins': [
            'cloudwatch = lemur_cloudwatch.plugin:CloudwatchMetricPlugin',
        ]
    }
)

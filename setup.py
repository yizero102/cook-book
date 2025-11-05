from setuptools import setup, find_packages

setup(
    name="multi_agent_system",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run_multi_agent_system=multi_agent_system.main:main',
        ],
    },
)

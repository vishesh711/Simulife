"""
SimuLife Package Setup
A Multi-Agent LLM Simulation where AI agents live, learn, form relationships, and build societies.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="simulife",
    version="1.0.0",
    author="SimuLife Development Team",
    author_email="dev@simulife.ai",
    description="A Multi-Agent LLM Simulation where AI agents live, learn, form relationships, and build societies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simulife-ai/simulife",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Sociology",
        "Topic :: Games/Entertainment :: Simulation",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "memory-profiler>=0.60.0",
            "psutil>=5.9.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.17.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "simulife=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "simulife": [
            "data/agent_configs/*.json",
            "docs/*.md",
        ],
    },
    keywords=[
        "artificial intelligence", "multi-agent simulation", "ai agents", 
        "llm", "society simulation", "behavioral modeling", "emergent behavior",
        "complex systems", "agent-based modeling", "social simulation"
    ],
    project_urls={
        "Bug Reports": "https://github.com/simulife-ai/simulife/issues",
        "Source": "https://github.com/simulife-ai/simulife",
        "Documentation": "https://simulife.readthedocs.io/",
    },
) 
"""项目安装配置文件"""

from setuptools import setup, find_packages

setup(
    name="gresy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    python_requires='>=3.6'
) 
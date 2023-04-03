from setuptools import setup

setup(
    name='hw_features',
    version='1.0.0',
    description='A library that detects handwriting features.',
    author='Joshua Fernandes',
    packages=['hw_features'],
    url="https://github.com/J0shuaFernandes/HandwritingFeatures",
    install_requires=['numpy', 'opencv-python'],
    python_requires='>=3.6'
)
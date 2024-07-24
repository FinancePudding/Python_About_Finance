from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zx_quant_tool',
    version='0.1.0',
    author='andy',
    author_email='andymax9444@gmail.com',
    description='量化分析工具包',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/FinancePudding/Python_About_Finance/tree/main/Quant%20Tool/zx_quant_tool',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'pandas',
        'numpy',
        'matplotlib',
        'exchange_calendars',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
)

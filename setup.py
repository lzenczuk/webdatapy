from setuptools import setup, find_packages

setup(
    name='webdatapy',
    version='0.1',
    description='Web data collecting and processing lib',
    url='http://github.com/lzenczuk/web_data',
    author='Lucjan Zenczuk',
    author_email='lucjan.zenczuk@gmail.com  ',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'pytz',
        'beautifulsoup4', 'nose'
    ]
)
import setuptools

long_description = '''
Share files on run any directory.

usage: sharefiles [port PORTNUMBER (Default 8000)] [--directory PATH (Default current directory)]

Alternatively run package as script:
    python -m sharefiles [port PORTNUMBER]

Go to http://localhost:8000/ or http://IP_ADDRESS:8000 on your favorite browser to download and upload files.

sharefiles -h for more info of usage

author: http://www.github.com/deduble/sharefiles

Supports everything the STL http.server does.
    Doc: https://docs.python.org/3/library/http.server.html

Credits: Densaugeo/uploadserver and python STL.
'''

setuptools.setup(
    name='sharefiles',
    version='0.0.1',
    author='deduble',
    author_email='yunus.kayalidere@gmail.com',
    description='A simple server, extended to allowing easy sharing file(s) to/from viewed directory.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/deduble/sharefiles',
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['sharefiles=sharefiles.command_line:main'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

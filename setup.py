import os.path

root = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(root, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='clipycube',
    version='1.0.0',
    description="Command line Rubik's cube",
    long_description=long_description,
    author='Mitch LeBlanc',
    author_email='supermitch@gmail.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Puzzle Games',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='commandline Rubiks cube',
)

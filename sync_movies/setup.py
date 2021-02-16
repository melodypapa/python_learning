from setuptools import setup, find_packages

setup(
    name='sync_movies',
    version = '1.0.0',
    license = 'proprietary',
    description="The utility for synchronizing the movies",

    author = 'Melody Papa',
    author_email = "melodypapa@outlook.com",
    url="melodypapa.github.io",

    packages = find_packages(where='src'),
    package_dir= {'': 'src'},

    install_requires=[],

    include_package_data=True,
    
    extras_require={'pytest': 'pytest-cov'},

    entry_points={
        'console_scripts': [
            'sync_movies      = sync_movies.cli.main:sync_movies_cli',
        ]
    }
)
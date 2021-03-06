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

    install_requires=['exifread', 'PyPDF2', 'requests', 'bs4', 'lxml', 'isbnlib'],

    include_package_data=True,
    
    extras_require={'pytest': 'pytest-cov'},

    entry_points={
        'console_scripts': [
            'sync-movies      = sync_movies.cli.main:sync_movies_cli',
            'sync-photos      = sync_photos.cli.main:sync_photos_cli',
            'sync-books       = sync_books.cli.main:sync_books_cli',
        ]
    }
)
# sync_movies

## Purpose

The utility for synchronizing the movies

## Unit test

Run `pip install pytest pytest-cov` to install pytest.

Run `pytest --cov=alvsetup --cov-report term-missing` to verify all the functionality.

## Create a distribution and wheel

Run `python setup.py sdist bdist_wheel` or `py -3 setup.py sdist bdist_wheel`

## CLI

### sync_movies

**synchronize the movies to the destination folder**

`sync_movies source destination -h`

```
-s source       The source folder of the movies
-d destination  The destination folder for the arranged movies.
-h              show the help information
```

### Example for sync_movies

```
sync_movies ~/Downloads/ /Volumes/EXT02/Movies/
```

## Release Notes

### 1.0.0 (Feb 14th 2021)

1. Add the synchronization features
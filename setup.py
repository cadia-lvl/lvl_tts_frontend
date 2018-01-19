try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'Description of the project',
    'author': 'Anna Björk Nikulásdóttir',
    'url': 'URL to get the project at',
    'download_url': 'Where to download it',
    'author_email': 'anna@skerpa.io',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'name of the project'
}

setup(**config)
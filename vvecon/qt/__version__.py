from typing import Dict, List

# Version Details:
__version__ = '0.0.1'
__title__ = 'Vvecon Qt Framework'
__project__ = 'Vvecon Qt Framework'
__last_update__ = '2024-11-08'
__author__ = ('Sasindu Wijethunga', )
__author_email__ = ('sasinduwijethunga@vvecon.com', )
__license__ = 'MIT License'
__url__ = ''
__description__ = 'Qt Framework for creating Qt applications'
__long_description__ = (
    'This is a Qt Framework by Vvecon. This is a framework for creating Qt applications. This '
    'framework is designed to be easy to use and easy to understand.')
__download_url__ = ''
__platforms__ = 'Windows, macOS, Linux'
__keywords__ = 'Qt Framework, Qt, PyQt5, PySide2, PySide6, Vvecon, Vvecon Qt Framework'
__classifiers__ = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: System :: Vvecon Qt Framework',
]
__entry_points__: Dict = {'console_scripts': []}
__extras_require__ = {
    'dev': [
        'pytest',
        'pytest-cov',
        'flake8',
        'black',
        'isort',
        'mypy',
        'sphinx',
        'sphinx-rtd-theme',
        'twine',
    ]
}
__install_requires__ = [
    'PyQt5',
    'requests',
    'pydub',
    'pyqt5-tools',
    'pyqt5-tools',
]
__python_requires__ = '>=3.11'
__scripts__: List[str] = []
__package_data__: Dict = {'vvecon': []}
__data_files__: List[str] = []

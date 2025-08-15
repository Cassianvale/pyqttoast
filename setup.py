from setuptools import setup, find_namespace_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    readme = '\n' + fh.read()

setup(
    name='pyqt-toast-enhanced',
    version='1.4.0',
    author='CassianVale',
    author_email='z1430066373@gmail.com',
    license='MIT',
    packages=find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'pyqttoast.css': ['*.css'],
        'pyqttoast.icons': ['*.png'],
        'pyqttoast.hooks': ['*.py']
    },
    install_requires=[
        'QtPy>=2.4.1'
    ],
    python_requires='>=3.7',
    description='Enhanced fork of pyqt-toast-notification with additional features and improvements',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Cassianvale/pyqttoast',
    project_urls={
        'Bug Reports': 'https://github.com/Cassianvale/pyqttoast/issues',
        'Source': 'https://github.com/Cassianvale/pyqttoast',
        'Original Project': 'https://github.com/niklashenning/pyqttoast',
    },
    keywords=['python', 'pyqt', 'qt', 'toast', 'notification', 'enhanced', 'fork'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ]
)

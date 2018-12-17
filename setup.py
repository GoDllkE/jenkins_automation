#!/usr/bin/env python2
"""
    Setup file for this module
"""
from setuptools import setup

setup(
    name='automation',
    version='5.1.6',
    packages=["automation"],
    url='https://stash.pontoslivelo.com.br/projects/JNK/repos/automation_role-strategy',
    download_url='https://stash.pontoslivelo.com.br/projects/JNK/repos/automation_role-strategy/archive/master.zip',
    description='A python module to automate project creations on jenkins.',
    author='Gustavo Toledo de Oliveira',
    author_email='gustavot53@gmail.com',
    keywords=['jenkins', 'automation', 'role-strategy', 'folders-plugin'],
    install_requires=['pyyaml', 'requests>=2.18.4', 'pyinstaller>=3.3', 'setuptools>=36.3'],
    classifiers=[
        # Intention
        'Intended Audience :: Developers',

        # Os requirement
        'Operating System :: OS Independent',

        # License
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Languages
        'Natural Language :: Portuguese (Brazilian)',

        # Supported versions
        'Programming Language :: Python :: 3.6'
    ],
    project_urls={
        'Source':
            'https://stash.pontoslivelo.com.br/projects/JNK/repos/automation_role-strategy',
        'Documentation':
            'https://stash.pontoslivelo.com.br/projects/JNK/repos/automation_role-strategy/docs',
        'Tracker':
            'https://stash.pontoslivelo.com.br/projects/JNK/repos/automation_role-strategy/issues'
    },
    long_description="""
    Jenkins Role-Strategy & Folders-Plus automation
    ========================================
    """)

'''
 scrapy project setup script
'''

import sys, os, os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import testscrapy

me = 'Samuel Luo'
memail = 'qi.dataintelligence@gmail.com'
packages = ['testscrapy','testscrapy.spiders','searchable']
setup (
    name='testscrapy',
    version=testscrapy.VERSION,
    zip_safe=True,
    description='testscrapy eggs',
    long_description=open('README.md','r').read(),
    author=me,
    author_email=memail,
    maintainer=me,
    maintainer_email=memail,
    url='',
    license='MIT',
    keywords=[''],
    packages=packages,
    # package_data=None,
    download_url='',
    platforms=['Independant'],
    classifiers = [
        'Programming Language :: Python',
        ],
    )

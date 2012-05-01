import os
from setuptools import setup, find_packages

setup(name='crom',
      version = '0.1dev',
      description="Components.",
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      license="BSD",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zope.interface',
                        'venusian',
                        'grokker'],
      extras_require = dict(
        test=['pytest >= 2.0'],
        ),
      entry_points="""
      # Add entry points here
      """,
      )

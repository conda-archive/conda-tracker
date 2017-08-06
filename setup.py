from setuptools import setup

setup(name='conda-tracker',
      version='0.1.0',
      author='Continuum Analytics',
      author_email='conda@continuum.io',
      description='Manage conda recipes',
      packages=['conda_tracker'],
      install_requires=[
        'click==6.7',
      ],
      entry_points='''
        [console_scripts]
        conda-tracker=conda_tracker.cli:cli
        ''',
      )

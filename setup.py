from setuptools import setup

setup(name='conda-tracker',
      version='0.1.1',
      author='Continuum Analytics',
      author_email='conda@continuum.io',
      description='Manage conda recipes',
      packages=['conda_tracker'],
      install_requires=[
        'click>=6.7',
        'GitPython>=2.1'
        'PyGithub>=1.3',
      ],
      entry_points='''
        [console_scripts]
        conda-tracker=conda_tracker.cli:cli
        ''',
      )

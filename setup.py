from distutils.core import setup
setup(
  name = 'dnaplotlib',
  packages = ['dnaplotlib'],
  version = '1.0',
  description = 'Genetic design visualization',
  author = 'Thomas Gorochowski, ',
  author_email = 'tom@chofski.co.uk',
  url = 'https://github.com/VoigtLab/dnaplotlib',
  download_url = 'https://github.com/VoigtLab/dnaplotlib/archive/1.0.tar.gz',
  keywords = ['visualization', 'SBOLv', 'genetic design', 'synthetic biology', 'systems biology'],
  classifiers = [],
  scripts=['apps/quick.py', 'apps/library_plot.py']
)

# http://peterdowns.com/posts/first-time-with-pypi.html
# http://stackoverflow.com/questions/14863785/pip-install-virtualenv-where-are-the-scripts

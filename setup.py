import sys
sys.path.insert(0, 'src/setuptools_ez518/shims')  # NOQA
import ez_518_pip; ez_518_pip.setup(__file__)

from setuptools import setup, find_packages


setup(
    name='setuptools_ez518',
    description='PEP-518 for setuptools',
    use_scm_version=True,
    package_dir={'': 'src'},
    packages=find_packages('src'),
)
from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='sevimon',
    version='0.2',
    license='LICENSE.txt',
    packages=[
      "sevimon",
      "sevimon.lib",
      "sevimon.lib.locale",
    ],
    package_dir={'sevimon': '', 'sevimon.lib': 'lib', 'sevimon.lib.locale': 'lib/locale'},
    entry_points = {
        'console_scripts': [
            'sevicfg=sevimon.sevicfg:main',
            'sevimon=sevimon.sevimon:main',
            'sevistat=sevimon.sevistat:main',
        ],
    },
    url='https://github.com/ioctl-user/sevimon',
    description='Self Video Monitoring tool for facial muscles.',
    keywords='sevimon face emotion tension stress muscles wrinkles',
    install_requires=requirements,
)

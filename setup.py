#!/usr/bin/env python

import os
import shutil
import stat

from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info

from mindaudio.version import __version__

version = __version__
package_name = 'mindaudio'
cur_dir = os.path.dirname(os.path.realpath(__file__))
pkg_dir = os.path.join(cur_dir, 'build')


def clean():
    # pylint: disable=unused-argument
    def readonly_handler(func, path, execinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists(os.path.join(cur_dir, 'build')):
        shutil.rmtree(os.path.join(cur_dir, 'build'), onerror=readonly_handler)
    if os.path.exists(os.path.join(cur_dir, f'{package_name}.egg-info')):
        shutil.rmtree(os.path.join(cur_dir, f'{package_name}.egg-info'), onerror=readonly_handler)


clean()


def update_permissions(path):
    """
    Update permissions.
    Args:
        path (str): Target directory path.
    """
    for dirpath, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            dir_fullpath = os.path.join(dirpath, dirname)
            os.chmod(dir_fullpath, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP)
        for filename in filenames:
            file_fullpath = os.path.join(dirpath, filename)
            os.chmod(file_fullpath, stat.S_IREAD)


class EggInfo(egg_info):
    """Egg info."""

    def run(self):
        super().run()
        egg_info_dir = os.path.join(cur_dir, f'{package_name}.egg-info')
        update_permissions(egg_info_dir)


class BuildPy(build_py):
    """BuildPy."""

    def run(self):
        super().run()
        mindarmour_dir = os.path.join(pkg_dir, 'lib', package_name)
        update_permissions(mindarmour_dir)


setup(
    name=package_name,
    version=version,
    author="MindLab-AI",
    url="https://github.com/mindlab-ai/mindaudio",
    project_urls={
        'Sources': 'https://github.com/mindlab-ai/mindaudio',
        'Issue Tracker': 'https://github.com/mindlab-ai/mindaudio/issues',
    },
    description="An open source computer vision research tool box.",
    license='Apache License 2.0',
    include_package_data=True,
    packages=find_packages(exclude=("mindaudio")),
    cmdclass={
        'egg_info': EggInfo,
        'build_py': BuildPy,
    },
    install_requires=[
        'numpy >= 1.17.0',
        'PyYAML >= 5.3',
        'tqdm',
        'Levenshtein'
    ]
)
print(find_packages())
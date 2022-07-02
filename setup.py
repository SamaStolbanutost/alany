import os
from setuptools import setup

setup(
    name='alany',
    version='0.1.0',
    description='''Programming language for creating bots in AnonyGram
                   and other programs.''',
    url='https://github.com/anony-oss/alany',
    install_requires=[],
    packages=['alany'],
    entry_points={'console_scripts': ['alany = alany.core:__main__']}
)

absolute = os.path.dirname(__file__)
path = absolute + '/std/'


if 'ALANY_PATH' in os.environ:
    command = f'export ALANY_PATH=$ALANY_PATH:{path}'
else:
    command = f'export ALANY_PATH={path}'
bash_profile_path = f'{os.getenv("HOME")}/.bash_profile'
with open(bash_profile_path, 'a') as file:
    file.write('\n' + command)

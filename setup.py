from setuptools import setup

setup(
    name='alany',
    version='0.1.2',
    description='''Programming language for creating bots in AnonyGram
                   and other programs.''',
    url='https://github.com/anony-oss/alany',
    install_requires=[],
    packages=['alany'],
    entry_points={'console_scripts': ['alany = alany.core:__main__']}
)

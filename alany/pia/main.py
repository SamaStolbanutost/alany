from git import Repo
import os
import shutil


def install(name, link=None):
    Repo.clone_from(link, f'{os.path.dirname(__file__)}/modules/{name}')


def update(name, link=None):
    remove(name)
    install(name=name, link=link)


def remove(name):
    shutil.rmtree(f'{os.path.dirname(__file__)}/modules/{name}')


update('alany', 'https://github.com/anony-oss/alany.git')
remove('alany')

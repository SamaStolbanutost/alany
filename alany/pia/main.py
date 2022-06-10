from git import Repo
import os
import shutil


def get_names():
    path = f'{os.path.dirname(__file__)}/lists/'
    files = [path + f for f in os.listdir(path) if os.path.isfile(path + f)]
    names = {}

    for file in files:
        with open(file, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                name = line.split('=')[0]
                value = line.split('=')[1]
                names[name] = value
    return names


def get_link(name, link):
    if link is None:
        names = get_names()
        return names[name]
    else:
        return link


def install(name, link=None):
    Repo.clone_from(get_link(name, link),
                    f'{os.path.dirname(__file__)}/modules/{name}')


def update(name, link=None):
    remove(name)
    install(name=name, link=link)


def remove(name):
    shutil.rmtree(f'{os.path.dirname(__file__)}/modules/{name}/')


# install('alany')

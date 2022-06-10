from git import Repo
import os


def clear(dir):
    files = [f for f in os.listdir(dir)
             if os.path.isfile(os.path.join(dir, f))]
    dirs = [f for f in os.listdir(dir)
            if not os.path.isfile(os.path.join(dir, f))]

    for file in files:
        os.remove(file)
    for dir in dirs:
        clear(dir)

    os.rmdir(dir)


def install(name, link=None):
    Repo.clone_from(link, f'{os.path.dirname(__file__)}/modules/{name}')


def update(name, link=None):
    remove(name)
    install(name=name, link=link)


def remove(name):
    clear(f'{os.path.dirname(__file__)}/modules/{name}')


update('alany', 'https://github.com/anony-oss/alany.git')
remove('alany')

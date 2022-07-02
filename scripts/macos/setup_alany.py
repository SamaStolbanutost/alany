import os

absolute = os.path.dirname(__file__)
path = absolute + '/std/'


if 'ALANY_PATH' in os.environ:
    command = f'export ALANY_PATH=$ALANY_PATH:{path}'
else:
    command = f'export ALANY_PATH={path}'
bash_profile_path = f'{os.getenv("HOME")}/.bash_profile'
with open(bash_profile_path, 'a') as file:
    file.write('\n' + command)

import os
import time

libs = [
    'netmiko',
]


def create_file(cmd):
    with open('installed_libs.txt', 'w+'):
        os.system('{} > installed_libs.txt'.format(cmd))


def check_libs():
    not_installed_libs = []
    for lib in libs:
        if lib in open('installed_libs.txt').read():
            print('{} is currently installed.'.format(lib))
        elif lib not in open('installed_libs.txt').read():
            not_installed_libs.append(lib)
            print(not_installed_libs)
    return not_installed_libs


def install_libs():
    for install in check_libs():
        os.system('pip3 install {}'.format(install))
        print(install)
    os.system('rm installed_libs.txt')


if __name__ == '__main__':
    create_file('pip list')
    install_libs()

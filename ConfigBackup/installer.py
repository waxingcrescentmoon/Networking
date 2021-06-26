import os
import time

libs = [
    'netmiko',
]

class InstallLibraries:

    not_installed_libs = []
    write_file = open('installed_libs.txt', 'w+')
    read_file = open('installed_libs.txt', 'r+')


    def create_file(cmd):
        with InstallLibraries.write_file:
            os.system('{} > installed_libs.txt'.format(cmd))


    def check_libs():
        for lib in libs:
            if lib not in InstallLibraries.read_file.read():
                InstallLibraries.not_installed_libs.append(lib)
                print("Not Installed: {}".format(InstallLibraries.not_installed_libs))
        return InstallLibraries.not_installed_libs


    def install_libs():
        for install in InstallLibraries.check_libs():
            os.system('pip3 install {}'.format(install))
        os.system('rm installed_libs.txt')


if __name__ == '__main__':
    InstallLibraries.create_file('pip list')
    InstallLibraries.install_libs()

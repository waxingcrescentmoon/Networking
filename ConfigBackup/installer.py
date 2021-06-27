import os
import time

libs = [
    'netmiko',
]

class InstallLibraries:

    not_installed_libs = []
    write_file = open('installed_libs.txt', 'w+')
    read_file = open('installed_libs.txt', 'r+')


    def create_file(cmd, txt):
        with InstallLibraries.write_file:
            os.system('{} > {}'.format(cmd, txt))


    def check_libs():
        for lib in libs:
            if lib in InstallLibraries.read_file.read():
                print('{} already installed'.format(lib))
            elif lib not in InstallLibraries.read_file.read():
                InstallLibraries.not_installed_libs.append(lib)
                print("Installed Libs: {}".format(InstallLibraries.not_installed_libs))
        return InstallLibraries.not_installed_libs


    def install_libs(txt):
        for install in InstallLibraries.check_libs():
            os.system('pip3 install {}'.format(install))
        os.system('rm {}'.format(txt))


if __name__ == '__main__':
    InstallLibraries.create_file('pip list', 'installed_libs.txt')
    InstallLibraries.install_libs('installed_libs.txt')

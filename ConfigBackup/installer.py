import os

libs = [
    'netmiko',
]

not_installed_libs = []


def check_libs():
    installed = 'pip list'
    line_list = []
    with open('installed_libs.txt', 'w+') as file:
        os.system(installed + ' > installed_libs.txt')
        for line in file:
            line_list.append(line)
    conjoin = ' '.join(line_list)
    return conjoin


def not_installed():
    conjoin = check_libs()
    for lib in libs:
        if lib in conjoin:
            print(lib + ' is currently installed.')
        elif lib not in conjoin:
            not_installed_libs.append(lib)
    return not_installed_libs


def install_libs():
    for install in not_installed():
        os.system('pip3 install {}'.format(install))
        os.system('rm installed_libs.txt')


if __name__ == '__main__':
    install_libs()

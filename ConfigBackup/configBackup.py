import getpass
import netmiko
import os
from installer import install_libs
from installer import create_file

"""
Update the network_addresses list to a range of
addresses that you want to pull configurations for.
"""
network_addresses = [
    '192.168.1.106',
    '10.10.10.1',
    '10.10.10.2',
    '10.10.10.3',
    '10.10.10.4',
    '10.10.10.5',
]

device_types = [
    'arista_eos',
    'aruba_os',
    'aruba_osswitch',
    'aruba_procurve',
    'broadcom_icos',
    'brocade_fastiron',
    'brocade_fos',
    'brocade_netiron',
    'brocade_nos',
    'brocade_vdx',
    'brocade_vyos',
    'ciena_saos',
    'cisco_asa',
    'cisco_ftd',
    'cisco_ios',
    'cisco_nxos',
    'cisco_s300',
    'cisco_tp',
    'cisco_wlc',
    'cisco_xe',
    'cisco_xr',
    'dell_dnos9',
    'dell_force10',
    'dell_isilon',
    'dell_os10',
    'dell_os6',
    'dell_os9',
    'dell_powerconnect',
    'extreme',
    'extreme_ers',
    'extreme_exos',
    'extreme_netiron',
    'extreme_nos',
    'extreme_slx',
    'extreme_vdx',
    'extreme_vsp',
    'extreme_wing',
    'fortinet',
    'hp_comware',
    'hp_procurve',
    'huawei',
    'huawei_olt',
    'huawei_smartax',
    'huawei_vrpv8',
    'juniper',
    'juniper_junos',
    'juniper_screenos',
    'netgear_prosafe',
    'paloalto_panos',
    'zte_zxros',
]

show_config_cmd = {
    'arista_eos': 'show running-config',
    'aruba_os': 'show running-config',
    'aruba_osswitch': 'show running-config',
    'aruba_procurve': 'show running-config',
    'broadcom_icos': 'full-configuration',
    'brocade_fastiron': 'full-configuration',
    'brocade_fos': 'full-configuration',
    'brocade_netiron': 'full-configuration',
    'brocade_nos': 'full-configuration',
    'brocade_vdx': 'full-configuration',
    'brocade_vyos': 'full-configuration',
    'ciena_saos': 'show running',
    'cisco_asa': 'show running-config',
    'cisco_ftd': 'show running-config',
    'cisco_ios': 'show running-config',
    'cisco_nxos': 'show running-config',
    'cisco_s300': 'show running-config',
    'cisco_tp': 'show running-config',
    'cisco_wlc': 'show running-config',
    'cisco_xe': 'show running-config',
    'cisco_xr': 'show running-config',
    'dell_dnos9': 'show running-config',
    'dell_force10': 'show running-config',
    'dell_isilon': 'show running-config',
    'dell_os10': 'show running-config',
    'dell_os6': 'show running-config',
    'dell_os9': 'show running-config',
    'dell_powerconnect': 'show running-config',
    'extreme': 'show config',
    'extreme_ers': 'show config',
    'extreme_exos': 'show config',
    'extreme_netiron': 'show config',
    'extreme_nos': 'show config',
    'extreme_slx': 'show config',
    'extreme_vdx': 'show config',
    'extreme_vsp': 'show config',
    'extreme_wing': 'show config',
    'fortinet': 'show config',
    'hp_comware': 'show running-config',
    'hp_procurve': 'show running-config',
    'huawei': 'display current-configuration',
    'huawei_olt': 'display current-configuration',
    'huawei_smartax': 'display current-configuration',
    'huawei_vrpv8': 'display current-configuration',
    'juniper': 'show configuration',
    'juniper_junos': 'show configuration',
    'juniper_screenos': 'show configuration',
    'paloalto_panos': 'show deviceconfig',
    'zte_zxros': 'show running-config',

}


def create_backup_directory():
    device_user = getpass.getuser()
    dir_path = '/Users/{}/Desktop/NetworkBackups'.format(device_user)
    if os.path.exists(dir_path):
        pass
    elif not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


def device_type_menu():
    """
    This should create a dictionary to associate the numbers in the menu to
    a device type
    """
    count = 1
    device_dictionary = {}
    for key, value in show_config_cmd.items():
        print("{}. {}".format(count, key))
        device_dictionary.update({str(count): str(key)})
        count = count + 1
    choose_device = str(input('Select the number corresponding to the type of device OS you are connecting to: '))
    return device_dictionary[choose_device]


def get_credentials():
    """
    Prompt for username and password.
    :return:
    """
    username = input('Enter Username: ')
    password = None
    while not password:
        password = getpass.getpass(prompt='Password: ')
        password_verify = getpass.getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match. Try again.')
            password = None
    return username, password


def running_config():
    username, password = get_credentials()
    device_type = device_type_menu()
    for device in network_addresses:
        try:
            net_connect = netmiko.ConnectHandler(ip=device,
                                                 device_type=device_type,
                                                 username=username,
                                                 password=password)
            print('~'*79)
            print('Connecting to device: ', device)
            hostname = ['show run | i hostname']
            running_config = show_config_cmd[device_type_menu()]
            output1 = net_connect.send_config_set(hostname)
            output2 = net_connect.send_config_set(running_config)
            file = open('/Users/{}/Desktop/NetworkBackups/{}'.format(device_user, output1), 'w+')
            file.write(' '.format(output2))
            print('Configurations written for {}'.format(device))
        except netmiko.ssh_exception.NetMikoTimeoutException as e:
            print('Failed to connect to', device, e)
        except netmiko.ssh_exception.NetMikoAuthenticationException as e:
            print('Failed to connect to', device, e)
        except TypeError as e:
            print('Failed to connect to', device, e)


if __name__ == '__main__':
    create_file('pip list')
    install_libs()
    create_backup_directory()
    running_config()

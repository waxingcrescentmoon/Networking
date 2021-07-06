import socket
from subprocess import Popen, PIPE
import re
import os
import sys

"""
Used to return the FQDN, IP Address and MAC Address
"""
# Import modules from subnet_calc.py to take user input and ping sweep a range of devices.
# Use the ping sweep to prevent users from modify this file with IP addresses.
IP = ["192.168.1.140", "192.168.1.130"]


class NetworkInfo:
    hostname_ip_mac = {}

    def verify_ip(ip):
        """
        Return True if the ip address has an entry in the arp table
        """
        check_ip = os.popen("arp -n {}".format(ip)).read()
        if "no entry" in check_ip:
            return False
        else:
            return True

    def update_arp(ip):
        return os.system('ping -c1 {} 2>&1 > /dev/null'.format(ip))

    def get_mac(ip):
        pid = Popen(["arp", "-n", ip], stdout=PIPE)
        s = pid.communicate()[0]
        s = s.decode("utf-8")
        mac = re.search(r"([0-9a-f]{2}(?::[0-9a-f]{2}){5})", s).groups()[0]
        return mac

    def get_hostname(ip):
        hostname = socket.getfqdn(ip)
        return hostname

if __name__ == '__main__':
    net_inf = NetworkInfo
    host = net_inf.hostname_ip_mac
    for ip in IP:
        if net_inf.verify_ip(ip) is True:
            host.update({net_inf.get_hostname(ip): (ip, net_inf.get_mac(ip))})
        elif net_inf.verify_ip(ip) is False:
            net_inf.update_arp(ip)
            host.update({net_inf.get_hostname(ip): (ip, net_inf.get_mac(ip))})
    print(net_inf.hostname_ip_mac)


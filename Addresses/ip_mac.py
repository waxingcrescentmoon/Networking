import socket
from subprocess import Popen, PIPE
import re
import os

"""
socket.getfqdn([name]) # Return the FQDN of lecal machine.
socket.gethostbyname(hostname) # Return Ip address with given hostname
socket.gethostbyaddr("1.1.1.1") # Return a triple (hostname, aliaslist, ipaddrlist) giddress
socket.gethostname() # Return a string containing the hostname of the machine where the Python interpreter is currently executing.
"""


IP = ["192.168.1.140","192.168.1.130"]

ip_mac = {}
# arp_table = os.system('arp -n {}'.format(IP))
for ip in IP:
    os.system('ping -c1 {} 2>&1 > /dev/null'.format(ip))
    pid = Popen(["arp", "-n", ip], stdout=PIPE)
    s = pid.communicate()[0]
    s = s.decode("utf-8")
    mac = re.search(r"([0-9a-f]{2}(?::[0-9a-f]{2}){5})", s).groups()[0]
    hostname = socket.getfqdn(ip)
    ip_mac.update({hostname:(ip, mac)})
print(ip_mac)
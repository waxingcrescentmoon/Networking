#! /usr/bin/python3
import sys
import re
from ipaddress import IPv4Network
"""
Quick network tasks to assit with network planning and implementation.
"""



class NetworkDetails:
    network = sys.argv[1]
    def available_bits():
        """
        Determine the number of available host bits based on CIDR input. This can be used
        to determine the number of available hosts in the subnet.

        """
        net = NetworkDetails.network
        index = net.index("/")
        index = index + 1
        available_bits = (32 - int((net[index:])))
        if available_bits in range(1, 32):
            return available_bits


    def num_hosts():
        """
        Take output of available_bits and return the number of hosts available on the subnet
        using the formula ((2**n)-2) or ((2**hostbits)-2).
        """
        num_bits = NetworkDetails.available_bits()
        num_hosts = ((2**num_bits - 2))
        return num_hosts



    def subnet_mask():
        """
        subnet_mask() uses get_mask(), which uses binary_count() to determine the subnet mask.
        """
        net = NetworkDetails.network
        index = net.index("/")
        index = index + 1
        bits_on = (int((net[index:])))

        if bits_on <= 8:
            octet_bits = NetworkDetails.get_mask(bits_on)
            return "{}.{}.{}.{}".format(octet_bits,0,0,0)
        if bits_on >= 9 and bits_on <= 16:
            bits_on = (bits_on - 8)
            octet_bits = NetworkDetails.get_mask(bits_on)
            return "{}.{}.{}.{}".format(255,octet_bits,0,0)
        if bits_on >= 17 and bits_on <= 24:
            bits_on = (bits_on - 16)
            octet_bits = NetworkDetails.get_mask(bits_on)
            return "{}.{}.{}.{}".format(255,255,octet_bits,0)
        if bits_on >= 25 and bits_on <= 32:
            bits_on = (bits_on - 24)
            octet_bits = NetworkDetails.get_mask(bits_on)
            return "{}.{}.{}.{}".format(255,255,255,octet_bits)


    def get_mask(bits_on):
        octet = NetworkDetails.binary_count(bits_on)
        sum_bits = 0
        for keys, values in octet.items():
            if values == 1:
                sum_bits = sum_bits + keys
        return sum_bits


    def binary_count(bits_on):
        """
        subnet_mask determines the Octet and octet_bits determines how many bits are on/off
        in the subnet mask.
        """
        octet = [
            128,
            64,
            32,
            16,
            8,
            4,
            2,
            1,
        ]
        bits_on = bits_on + 1
        bit_cache = []
        for bit in range(1, bits_on):
            bit = 1
            bit_cache.append(bit)
        bits_on_off = dict(zip(octet, bit_cache))
        return bits_on_off



class Subnetting:
    #network = IPv4Network(sys.argv[1])

    def subnet_mask():
        """
        Return the Subnet Mask.
        :return:
        """
        return Subnetting.network.netmask
    def net_id():
        """
        Return the Network ID

        """
        return Subnetting.network.network_address
    def broacast_id():
        """
        Return the Broadcast ID.
        :return:
        """
        return Subnetting.network.broadcast_address


if __name__ == '__main__':
    try:
        print("Subnet Mask: {}".format(NetworkDetails.subnet_mask()))
        print("Number of hosts: {}".format(NetworkDetails.num_hosts()))
    except ValueError:
        print("""
        Please input an appropriate value using CIDR notation. 
        Ex.) 10.1.1.1/26
        """)
    except TypeError:
        print("""
                Please input an appropriate value using CIDR notation. 
                Ex.) 10.1.1.1/26
                """)

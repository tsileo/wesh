#!/usr/bin/env python

""" Example of announcing a service (in this case, a fake HTTP server) """

import logging
import socket
import sys
import fcntl
import struct
from time import sleep

from zeroconf import ServiceInfo, Zeroconf
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def get_hostname():
    hostname = socket.gethostname()
    if hostname.endswith('.local'):
        return hostname

    return hostname + '.local'


def get_ip_address(ifname='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

zeroconf = Zeroconf()
services = []


def add_service(name, port, desc={}):
    info = ServiceInfo("_http._tcp.local.",
                       "{}._http._tcp.local".format(name),
                       socket.inet_aton(get_ip_address()), port, 0, 0,
                       desc, "{}.local.".format(get_hostname()))
    zeroconf.register_service(info)
    services.append(info)


# TODO(tsileo): loads from YAML

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {}
    print("Registration of a service, press Ctrl-C to exit...")
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        for service in services:
            zeroconf.unregister_service(service)
        zeroconf.close()

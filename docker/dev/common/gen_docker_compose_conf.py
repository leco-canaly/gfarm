#! /usr/bin/env python3

from ipaddress import IPv4Network, IPv6Network
from os import environ
import sys

num_gfmds = int(environ['GFDOCKER_NUM_GFMDS'])
num_gfsds = int(environ['GFDOCKER_NUM_GFSDS'])
num_clients = int(environ['GFDOCKER_NUM_CLIENTS'])
ip_version = environ['GFDOCKER_IP_VERSION']
subnet = environ['GFDOCKER_SUBNET']
start_host_addr = int(environ['GFDOCKER_START_HOST_ADDR'])
hostname_prefix_gfmd = environ['GFDOCKER_HOSTNAME_PREFIX_GFMD']
hostname_prefix_gfsd = environ['GFDOCKER_HOSTNAME_PREFIX_GFSD']
hostname_prefix_client = environ['GFDOCKER_HOSTNAME_PREFIX_CLIENT']
hostname_suffix = environ['GFDOCKER_HOSTNAME_SUFFIX']

hostport_s3_http = environ['GFDOCKER_HOSTPORT_S3_HTTP']
hostport_s3_https = environ['GFDOCKER_HOSTPORT_S3_HTTPS']

if ip_version == '4':
    nw = IPv4Network(subnet)
elif ip_version == '6':
    nw = IPv6Network(subnet)
else:
    sys.exit('invalid syntax: GFDOCKER_IP_VERSION')

class ContainerHost:
    def __init__(self, name, ipaddr):
        self.name = name
        self.hostname = name + hostname_suffix
        self.ipaddr = ipaddr

hi = nw.hosts()
hosts = []

for i in range(0, start_host_addr - 1):
    next(hi)  # skip unused hosts

# pin IP address for client1
for i in range(0, num_clients):
    hosts.append(ContainerHost(
        '{}{}'.format(hostname_prefix_client, i+1),
        next(hi)
    ))
for i in range(0, num_gfmds):
    hosts.append(ContainerHost(
        '{}{}'.format(hostname_prefix_gfmd, i+1),
        next(hi)
    ))

for i in range(0, num_gfsds):
    hosts.append(ContainerHost(
        '{}{}'.format(hostname_prefix_gfsd, i+1),
        next(hi)
    ))


print('''\
# This file was automatically generated.
# Do not edit this file.

version: "3.4"

x-common:
  &common
  image: gfarm-dev:${GFDOCKER_PRJ_NAME}
  volumes:
    - ./mnt:/mnt:rw
    - /sys/fs/cgroup:/sys/fs/cgroup:ro
  security_opt:
    - seccomp:unconfined
    - apparmor:unconfined
  cap_add:
    - SYS_ADMIN
    - SYS_PTRACE
  devices:
    - /dev/fuse:/dev/fuse
  privileged: false
  extra_hosts:
''', end='')

for h in hosts:
    print("    - {}:{}".format(h.hostname, str(h.ipaddr)))
    print("    - {}:{}".format(h.name, str(h.ipaddr)))

print('''\

services:
''', end='')

if hostport_s3_http and hostport_s3_https:
    client1_ports = '''
    ports:
      - {}:80
      - {}:443'''.format(int(hostport_s3_http), int(hostport_s3_https))
else:
    client1_ports = ''

for h in hosts:
    ports = '';
    if h.name == 'client1':
        ports = client1_ports
    print('''\
  {}:
    hostname: {}{}
    networks:
      gfarm_dev:
        ipv{}_address: {}
    <<: *common

'''.format(h.name, h.hostname, ports, ip_version, str(h.ipaddr)), end='')

print('''\

networks:
  gfarm_dev:
    name: gfarm_dev
    external: false
    ipam:
      config:
        - subnet: {}
'''.format(subnet), end='')

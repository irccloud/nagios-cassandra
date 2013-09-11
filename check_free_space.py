#!/usr/bin/env python
from __future__ import division, absolute_import, print_function, unicode_literals
import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='Check the free space of a Cassandra cluster via Opscenter')

parser.add_argument('-n', metavar='CLUSTER', required=True)
parser.add_argument('-o', metavar='OPSCENTER-URL', required=True)
parser.add_argument('-w', metavar='WARN', type=int, default=70)
parser.add_argument('-c', metavar='CRIT', type=int, default=90)

args = parser.parse_args()

url = "%s/%s/storage-capacity" % (args.o, args.n.replace(' ', '_'))
result = requests.get(url)

if result.status_code != 200:
    print('STATE UNKNOWN: URL %s returned HTTP code %s' % (url, result.status_code))
    sys.exit(3)

data = result.json()

pc = (data['used_gb'] / (data['used_gb'] + data['free_gb'])) * 100

if pc > args.c:
    print('STATE CRITICAL: Cluster is %.2f%% full' % pc)
    sys.exit(2)
elif pc > args.w:
    print('STATE WARNING: Cluster is %.2f%% full' % pc)
    sys.exit(1)
else:
    print('STATE OK: Cluster is %.2f%% full' % pc)
    sys.exit(0)

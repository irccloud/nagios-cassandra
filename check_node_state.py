#!/usr/bin/env python
from __future__ import division, absolute_import, print_function, unicode_literals
import requests
import argparse
import sys

parser = argparse.ArgumentParser(description='Check the liveness of a Cassandra node via Opscenter')

parser.add_argument('-H', metavar='HOST', required=True)
parser.add_argument('-n', metavar='CLUSTER', required=True)
parser.add_argument('-o', metavar='OPSCENTER-URL', required=True)
parser.add_argument('-w', metavar='WARN', type=int, default=30)
parser.add_argument('-c', metavar='CRIT', type=int, default=120)

args = parser.parse_args()

url = "%s/%s/nodes/%s/last_seen" % (args.o, args.n.replace(' ', '_'), args.H)
result = requests.get(url)

if result.status_code != 200:
    print('STATE UNKNOWN: URL %s returned HTTP code %s' % (url, result.status_code))
    sys.exit(3)

age = int(result.text)

if age > args.c:
    print('STATE CRITICAL: node %s was last seen %s seconds ago' % (args.H, age))
    sys.exit(2)
elif age > args.w:
    print('STATE WARNING: node %s was last seen %s seconds ago' % (args.H, age))
    sys.exit(1)
else:
    print('STATE OK: node %s was last seen %s seconds ago' % (args.H, age))
    sys.exit(0)

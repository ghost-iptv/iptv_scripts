#!/usr/bin/env python
from mac_generator import generate_macs
for mac in generate_macs(mac='00:1a:79:5x:ef:X2',case='lower',combs=None, random=True):
 print(mac)

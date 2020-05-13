#!/usr/bin/env python
from random import randint
from itertools import count


def xrange(stop):
    try:
        return iter(count().next, stop)
    except Exception:
        return range(stop)


def option(mac, case, num=None):
    if num:
        if case == 'upper':
            return num.upper()
        return num.lower()
    if case == 'upper':
        mac = mac.upper()
        x = mac.count('X')
        form = mac.replace('X', '{}')
    else:
        mac = mac.lower()
        x = mac.count('x')
        form = mac.replace('x', '{}')
    return (mac, x, form)


def generate_macs(mac='00:1a:79:xx:xx:XX', case='lower', combs=None, random=False):
    """
    combs   | integer |   if combs=None max_combs is calculated automatically, max_combs is equal to 16**x , where x is number of "x" in mac_address string
    random  | bool    |   [True,False] if set to False this order is used [0,1,3,4,5,6,7,8,9,a,b,c,d,e,f]
    case    | string  |   ["lower","upper"]
    mac     | string  |  '00:1a:79:xx:xx:XX',  12 hex digits [0,1,3,4,5,6,7,8,9,a,b,c,d,e,f] in 6 pairs by 2 [mac={}{}:{}{}:{}{}:{}{}] with ":" as separators between pairs.
    Use "X" or "x" to set Unknown digit


    USAGE (for example):

    from macs_by_losmij import generate_macs
    for mac in generate_macs(mac='00:1a:79:5x:ef:X2',case='lower',combs=None, random=True):
        print(mac)"""
    mac, x, form = option(mac, case)
    combs = combs if combs else 16 ** x
    for num in xrange(combs):
        if random:
            num = randint(0, combs)
        hex_num = option('', case, num=hex(num)[2:].zfill(x))
        mac = form.format(*hex_num)
        yield mac


if __name__ == "__main__":
    help(generate_macs)

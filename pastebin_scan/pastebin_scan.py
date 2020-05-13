#!/usr/bin/env python
import os
import time
try:
    import requests
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

var = {'api': '', 'found': 0}


def cls(): os.system('cls' if os.name == 'nt' else 'clear')


def wait(sleep):
    for i in range(0, sleep):
        t = sleep-i
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        cls()
        print ('Found:{} | {}'.format(
            var['found'], "Time until next schedule scan:   %d:%02d:%02d" % (h, m, s)))
        time.sleep(1)


def scrape(triggers, api, path):
    try:
        api = requests.get(api, verify=False).text.splitlines()
        var['api'] = api[0]
        j = 0
        for url in api[1::]:
            j += 1
            cls()
            print ('Found:{} | Url:{} | API_Time:{} | Progress:{}/{}'.format(
                var['found'], url, var['api'], j, len(api[1::])))
            filename = url.split('/')[-1]
            try:
                r = requests.get(url, verify=False).text
                if any(trigger in r for trigger in triggers):
                    var['found'] = var['found']+1
                    if os.path.isdir(path) is not True:
                        os.makedirs(path)
                    with open(os.path.join(path, filename+'.txt'), 'w+') as f:
                        f.write('Url:{}\n\n{}'.format(url, r))
            except Exception:
                pass
    except Exception:
        pass


def pastebin_scan(triggers=['.ts', '/udp/', 'EXTINF', 'deviceMac', 'deviceUser', '00:1A:79', '&uid=', '.m3u8'],
                  api='https://epg.serbianforum.org/rest/pastebin.txt', path='results', sleep=300):
    while True:
        scrape(triggers, api, path)
        wait(sleep)


if __name__ == "__main__":
    pastebin_scan()

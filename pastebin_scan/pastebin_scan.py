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

var = {'api': '', 'found': 0, 'ide': ''}


def cls():
    if not var['ide']:
        os.system('cls' if os.name == 'nt' else 'clear')


def wait(sleep):
    for i in range(0, sleep):
        t = sleep-i
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        cls()
        print ('Found:{} | {}'.format(
            var['found'], "Time until next schedule scan:   %d:%02d:%02d" % (h, m, s)))
        time.sleep(1)


def scrape(triggers, api, path, match):
    match = all if match == 'all' else any
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
                if match(trigger in r for trigger in triggers):
                    var['found'] = var['found']+1
                    if os.path.isdir(path) is not True:
                        os.makedirs(path)
                    with open(os.path.join(path, filename+'.txt'), 'w+') as f:
                        f.write('Url:{}\n\n{}'.format(url, r.encode('utf8')))
            except Exception:
                pass
    except Exception:
        pass


def pastebin_scan(triggers=['http', '.m3u8'], api='https://epg.serbianforum.org/rest/pastebin.txt', path='results', sleep=600, match=all, ide=False):
    """
    triggers| list    |   List of words to be match in pastebin file
    api     | string  |   An api URL that cointains scraped raw urls, uses premium account and Whitelisted IP to avoid getting blocked
    path    | string  |   A odirectory path that contains scanning results
    sleep   | integer |   An integer that defines waiting time in SECONDS until next scan is started. To avoid IP ban set it min to 5 minuts (sleep=300)
    match   | method  |   [all,any]. Bulit in method,  all()-all elements in the given iterable are found, any()- any element is found
    ide     | bool    |   [True,False]. If set to True, python should stop clearing screen on IDE consoles and a terminal.
    """
    var['ide'] = ide
    while True:
        scrape(triggers, api, path, match)
        wait(sleep)


if __name__ == "__main__":
    pastebin_scan()

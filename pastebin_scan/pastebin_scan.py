#!/usr/bin/env python
import os
import time
from traceback import format_exc as log_error
try:
    import requests
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

var = {'refreshed': '', 'found': 0, 'console': ''}


def cls():
    if var['console']:
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


def scrape(triggers, match, timeout, api, path):
    match = all if match == 'all' else any
    try:
        api = requests.get(api, verify=False).text.splitlines()
        var['api'] = api[0]
        j = 0
        for url in api[1::]:
            j += 1
            cls()
            print ('Found:{} | Url:{} | API_refreshed:{} | Progress:{}/{}'.format(
                var['found'], url, var['refreshed'], j, len(api[1::])))
            filename = url.split('/')[-1]
            try:
                r = requests.get(url, verify=False).text
                if match(trigger in r for trigger in triggers):
                    var['found'] = var['found']+1
                    if os.path.isdir(path) is not True:
                        os.makedirs(path)
                    with open(os.path.join(path, filename+'.txt'), 'w+') as f:
                        f.write('Url:{}\n\n{}'.format(url, r.encode('utf8')))
                time.sleep(timeout)
            except Exception:
                print (log_error)
    except Exception:
        print (log_error)


def pastebin_scan(triggers=['.m3u8'], match=any, timeout=1, api='https://epg.serbianforum.org/rest/pastebin.txt', path='pastebin_results', sleep=600, console=True):
    """
    triggers| list    |   List of words to be match in pastebin file
    match   | method  |   [all,any]. Bulit in method,  all()-all elements in the given iterable are found, any()- any element is found
    timeout | integer |   An integer that defines time in SECONDS until next scan is started. *To avoid getting IP ban set timeout=>1
    api     | string  |   An api URL that cointains scraped raw urls, uses premium account and Whitelisted IP to avoid getting blocked
    path    | string  |   A odirectory path that contains scanning results
    sleep   | integer |   An integer that defines waiting time in SECONDS until next scan is started. *To avoid getting IP ban set sleep=>600
    console | bool    |   [True,False]. If set to False, python should print line by line and stop clearing screen on IDE console and a terminal.
    """
    var['console'] = console
    while True:
        scrape(triggers, match, timeout, api, path)
        wait(sleep)


if __name__ == "__main__":
    pastebin_scan(triggers=['m3u', '.ts', '/udp/', 'EXTINF', 'url', 'deviceMac',
                            'deviceUser', 'MAC:00:1A:79', '&uid='], match=any, timeout=1, sleep=600)

#!/usr/bin/env python3
from scapy.all import *
import socket, urllib3, re, os, time, shutil, codecs, psutil

CACHE_TIME = 86400  # 24 hours expressed in seconds
CACHE_FILE = os.path.join(os.getcwd(), ".oui-cache")
COMPANY_NAME = 'Raspberry'
url = 'https://standards-oui.ieee.org/oui/oui.txt'

def mac_to_oui(m):
    oui = "-".join(m.split(':')[:3])
    return(oui.upper())


def output_identifiers(file, string):
    matches = []
    with codecs.open(file,'r',encoding='utf8') as oui_list:
        for line in iter(oui_list):
            if re.search(string, line, re.IGNORECASE):
                if "-" in line: # we only want lines that contain the hex OUI
                    matches.append(line[0:8])
    return(matches)

def update_cache(u):
    http = urllib3.PoolManager()
    r = http.request('GET', u, preload_content=False)

    with open(CACHE_FILE, 'wb') as outfile:
        shutil.copyfileobj(r, outfile)

        r.release_conn()
    print('Cache updated.')

if __name__ == "__main__":
    print(f'Looking for raspberri pis.')
    # Lets not hammer a free service.
    try:
        if time.time() - os.stat(CACHE_FILE).st_ctime > CACHE_TIME:
            print(f"Updating the cache from {url}")
            update_cache(url)
        else:
            print(f'Local cache is present and less than {CACHE_TIME} seconds old. Skiped update.')
    except FileNotFoundError as err:
        print(f"Updating the cache from {url}")
        update_cache(url)
    
    matching_oui_list = output_identifiers(CACHE_FILE, COMPANY_NAME)

    ans,unans = arping("10.23.23.0/24", verbose=0)
    for s,r in ans:
        if mac_to_oui(r[Ether].src) in matching_oui_list:
            print("{} {}".format(r[Ether].src,s[ARP].pdst))

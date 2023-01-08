#!/usr/bin/env python3
from scapy.all import *
import urllib3, re, os, time, shutil, codecs, subprocess

CACHE_TIME = 86400  # 24 hours expressed in seconds
CACHE_FILE = os.path.join(os.getcwd(), ".oui-cache")
COMPANY_NAME = 'Raspberry'
url = 'https://standards-oui.ieee.org/oui/oui.txt'

def get_network_cidr():
    # Get the ethernet adapter name
    output = subprocess.run(["ip", "route", "get", "1"], capture_output=True)
    output_str = output.stdout.decode("utf-8")
    ip_address = output_str.split()[6]
    default_iface = output_str.split()[4]
    
    cmd = f"ip route | grep src | grep {default_iface} | awk '{{print $1}}'"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return(output.decode('utf-8'))
    

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
            print(f'Local cache is present and less than {CACHE_TIME} seconds old. Skipped update.')
    except FileNotFoundError as err:
        print(f"Updating the cache from {url}")
        update_cache(url)
    
    matching_oui_list = output_identifiers(CACHE_FILE, COMPANY_NAME)

    ignore_ifaces_list = ['lo', 'docker0']
    network_cidr = get_network_cidr()
    ans,unans = arping(network_cidr.strip(), verbose=0)
    print(f"List of located RPIs on network: {network_cidr}")
    for s,r in ans:
        if mac_to_oui(r[Ether].src) in matching_oui_list:
            print("{} {}".format(r[Ether].src,s[ARP].pdst))

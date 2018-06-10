#!/usr/bin/env python3

import logging
import godaddypy
import requests
import json

from settings import *
from settings_local import *

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# get current IP-addresses
ipv4 = False
ipv6 = False
try:
    ipv4 = requests.get('https://v4.ident.me/').content.decode()
except requests.exceptions.ConnectionError:
    logging.warn('GoDaddyUpdater: Cannot get current IPv4-Address')

try:
    ipv6 = requests.get('https://v6.ident.me/').content.decode()
except requests.exceptions.ConnectionError:
    logging.warn('GoDaddyUpdater: Cannot get current IPv6-Address')

# call godaddy api
account = godaddypy.Account(
    api_key=GODADDY_PUBLIC_KEY,
    api_secret=GODADDY_SECRET_KEY
)
client = godaddypy.Client(account)

for domain, subdomains in DOMAINS.items():
    if isinstance(subdomains, str):
        subdomains = [subdomains]

    if isinstance(subdomains, bool) and subdomains == True:
        subdomains = ['@']

    new_records = []
    for subdomain in subdomains:
        if ipv4:
            new_records.append({'data': ipv4, 'name': subdomain, 'ttl': DOMAIN_TTL, 'type': 'A'})
        if ipv6:
            new_records.append({'data': ipv6, 'name': subdomain, 'ttl': DOMAIN_TTL, 'type': 'AAA'})

    current_records = client.get_records(domain)

    for new in new_records:
        current = list(filter(lambda r: r['name'] == new['name'] and r['type'] == new['type'], current_records))
        if not current or new != current[0]:
            try:
                if not current:
                    client.add_record(domain, new)
                    logging.info('GoDaddyUpdater: Record for {0} created: {1}'.format(domain, json.dumps(new)))
                else:
                    client.update_record(domain, new)
                    logging.info('GoDaddyUpdater: Record for {0} updated: {1}'.format(domain, json.dumps(new)))

            except godaddypy.client.BadResponse as e:
                logging.error(
                    'GoDaddyUpdater: Record for {0} cannot set to {1}: {2}'.format(domain, json.dumps(new), e.__str__())
                )
        else:
            logging.info('GoDaddyUpdater: Record for {0} was already up-to-date: {1}'.format(domain, json.dumps(new)))

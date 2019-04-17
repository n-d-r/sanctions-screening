#===============================================================================
# Setup
#===============================================================================

import requests

#===============================================================================
# Constants
#===============================================================================

SDN_LIST_URL = 'https://www.treasury.gov/ofac/downloads/sanctions/1.0/sdn_advanced.xml'
CON_LIST_URL = 'https://www.treasury.gov/ofac/downloads/sanctions/1.0/cons_advanced.xml'
NUM_RETRIEVAL_ATTEMPTS = 3

#===============================================================================
# Functions
#===============================================================================

def retrieve_url(url, num_attempts=NUM_RETRIEVAL_ATTEMPTS):
  attempts = 0
  while attempts < num_attempts:
    r = requests.get(url)
    if r.status_code == 200:
      print('[+] successfully retrieved url: {url}'.format(url))
      return r
    else:
      attempts += 1
  print('[-] could not retrieve url: {url}'.format(url))
  return None

#===============================================================================
# Downloading the data
#===============================================================================

sdn = retrieve_url(url=SDN_LIST_URL)
con = retrieve_url(url=CON_LIST_URL)

if sdn:
  with open('sdn_list.xml', 'wb') as outfile:
    outfile.write(sdn.content)

if con:
  with open('con_list.xml', 'wb') as outfile:
    outfile.write(con.content)    
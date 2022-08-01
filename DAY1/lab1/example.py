import requests
from pprint import PrettyPrinter

# disable warnings about self-signed certs
import urllib3
urllib3.disable_warnings()

# USE YOUR IPs
DEVICE_IPS = ['192.168.0.10',
              '192.168.0.11',
              '192.168.0.12',
              '192.168.0.13',
              '192.168.0.14',
              '192.168.0.15',
              '192.168.0.16',
              '192.168.0.17',
              '192.168.0.18'
              ]

#SAMPLE_IP = ['192.168.0.10']

# USE YOUR ATD CREDENTIALS 
USERNAME = 'arista'
PASSWORD = 'aristaum4t'

if __name__ == '__main__':
  for ip in DEVICE_IPS:
    payload = {'jsonrpc': '2.0',
               'method': 'runCmds',
               'params': {
                 'version': 1,
                 # commands to run
                 'cmds': ["show hostname", "show version"]
               },
               'id': '1'
              }
    pp = PrettyPrinter()
    r = requests.post('https://{}:443/command-api'.format(ip), json=payload, auth=(USERNAME, PASSWORD), verify=False)
    response = r.json()
    result = response["result"]
    showHostname = result[0]
    showVersion = result[1]
    print(f"{showHostname['fqdn']} is a {showVersion['modelName']} with serial number {showVersion['serialNumber']} and system MAC address {showVersion['systemMacAddress']}")

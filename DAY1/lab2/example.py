import requests
from jinja2 import Environment, FileSystemLoader
from pprint import PrettyPrinter

# disable warnings about self-signed certs
import urllib3
urllib3.disable_warnings()

DEVICE_IPS = ['192.168.0.10',
              '192.168.0.11',
              '192.168.0.12',
              '192.168.0.13',
              '192.168.0.14',
              '192.168.0.15',
              '192.168.0.16',
              '192.168.0.17',
              ]
              
# USE YOUR CREDENTIALS
USERNAME = 'arista'
PASSWORD = 'aristaum4t'

if __name__ == '__main__':
    payload = {'jsonrpc': '2.0',
               'method': 'runCmds',
               'params': {
                 'version': 1,
                 'cmds': ['show version',
                          'show hostname',
                          'show ip arp']
               },
               'id': '1'
              }
    device_outputs = {}

    pp = PrettyPrinter()
    env = Environment(loader=FileSystemLoader("/home/coder/project/LABFILES/DAY1/lab2"))
    template = env.get_template("example.j2")

    for device in DEVICE_IPS:
        r = requests.post('https://{}:443/command-api'.format(device), json=payload, auth=(USERNAME, PASSWORD), verify=False)
        response = r.json()
        result = response["result"]

        showVersion = result[0]
        showHostname = result[1]
        showIpArp = result[2]
        #['show version','show hostname','show ip arp']
        # device_outputs[hostname] = object{'serial':serial, 'arpTable': []}
        
        device_outputs[showHostname['hostname']] = {'serial': showVersion['serialNumber'], 'ARP': [(entry["address"], entry["hwAddress"], entry["interface"]) for entry in showIpArp["ipV4Neighbors"]]}
        # figure out how to store the ARP address table data in a way that will make your template rendering easy
    else:
        #print(device_outputs)
        #pp.pprint(device_outputs)
        print(template.render(devices=device_output))
        pass
    
import requests
from jinja2 import Environment, FileSystemLoader
from pprint import PrettyPrinter

# disable warnings about self-signed certs
import urllib3
urllib3.disable_warnings()

CVP_IP = "tac-avd-v2-11-0185b69f.topo.testdrive.arista.com"
              
# USE YOUR CREDENTIALS
USERNAME = 'arista'
PASSWORD = 'aristaum4t'

if __name__ == '__main__':
    pp = PrettyPrinter()
    env = Environment(loader=FileSystemLoader("/home/coder/project/LABFILES/DAY1/lab3"))
    template = env.get_template("pretty.j2")

    with open('/home/coder/project/LABFILES/DAY1/lab3/token') as infile:
        access_token = infile.read()

    s = requests.session()
    s.verify = False
    s.cookies.set("access_token", access_token)

    # change imageurl to the actual endpoint you find in the REST API explorer
    r = s.get('https://{}/cvpservice/image/getImages.do?startIndex=0&endIndex=0'.format(CVP_IP))
    getImagesJSON = r.json()

    # change containerurl to the actual endpoint you find in the REST API explorer
    r = s.get('https://{}/cvpservice/inventory/containers'.format(CVP_IP))
    getContainersJSON = r.json()

    images = [] # arr of object 
    containers = [] # arr of objects

    for image in getImagesJSON["data"]:
        images.append({"name": image["name"] })
    
    for container in getContainersJSON:
        containers.append({"name": container["Name"]})

    print(images, containers)

    print(template.render(images=images, containers=containers))
    # pass the data you collected above to your jinja tempalte
   # print(template.render(kwargs=kwargs))
    #print(template.render())
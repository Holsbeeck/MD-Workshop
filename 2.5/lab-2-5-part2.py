import json
import requests
from netmiko import ConnectHandler
requests.packages.urllib3.disable_warnings()

api_url = "https://192.168.56.4/restconf/data/ietf-interfaces:interfaces/interface=Loopback99"

headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }

basicauth = ("cisco", "cisco123!")

yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback99",
        "description": "WHATEVER99",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "99.99.99.99",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

resp = requests.put(api_url, data=json.dumps(yangConfig),
                    auth=basicauth, headers=headers, verify=False)
if (resp.status_code >= 200 and resp.status_code <= 299):
    print("STATUS OK: {}".format(resp.status_code))
else:
    print("Error code {}, reply: {}".format(resp.status_code, resp.json()))

sshCli = ConnectHandler(
    device_type='cisco_ios',
    host='192.168.56.4',
    port='22',
    username='cisco',
    password='cisco123!'
)

output = sshCli.send_command("show ip int brief")
print("show ip int biref:\n{}\n".format(output))

resp = requests.delete(api_url, data=json.dumps(yangConfig),
                       auth=basicauth, headers=headers, verify=False)
if (resp.status_code >= 200 and resp.status_code <= 299):
    print("STATUS OK: {}".format(resp.status_code))
else:
    print("Error code {}, reply: {}".format(resp.status_code, resp.json()))

output = sshCli.send_command("show ip int brief")
print("show ip int biref:\n{}\n".format(output))

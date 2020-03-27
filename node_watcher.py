import json
import requests


user=''
passwd=''
payload = {"method": "getpeerinfo", "params": []}
def main():
    response = requests.post("https://prod.zaujec.tech:8331",data=json.dumps(payload), auth=(user, passwd))
    for node in response.json()['result']:
        print(f"ADDRESS: {node['addr']} VERSION: {node['version']} AGENT: {node['subver']}")


if __name__ == "__main__":
    main()

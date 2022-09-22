import requests, json

url = 'http://localhost:8110'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def sendCmd(cmd, dur):
    global url
    global headers
    data = {'cmd' : cmd, 'dur': str(dur)}
    x = requests.post(url.encode('utf-8'), data={'payload':json.dumps(data)}, headers=headers)
    print(x.text)

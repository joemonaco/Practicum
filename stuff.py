import requests
import json
import ast


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://cloud.rapsodo.com/2.1/',
    'Origin': 'http://cloud.rapsodo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Content-Type': 'application/json',
}

data = '{"email":"ccollazo@monmouth.edu","password":"mubaseball"}'

response = requests.post(
    'https://cloud.rapsodo.com/v2/auth/login', headers=headers, data=data)

# print(str(response.json()))

JWT = response.json()['token']


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://cloud.rapsodo.com/2.1/',
    'Origin': 'http://cloud.rapsodo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Authorization': JWT,
    'Sec-Fetch-Mode': 'cors',
    'Filter': '{"sport":2,"combine":1,"coaches":[1102083,1102645],"groups":[]}',
}

response = requests.get(
    'https://cloud.rapsodo.com/v2/pitching/team-players', headers=headers)

# print response.json()

# print str(response.json())

stuff = response.json()

# print(ast.literal_eval(json.dumps(stuff)))

#
print(json.dumps(stuff))

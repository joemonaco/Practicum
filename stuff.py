import requests
import json
import ast


authenticationHeaders = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://cloud.rapsodo.com/2.1/',
    'Origin': 'http://cloud.rapsodo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
    'Content-Type': 'application/json',
}

authenticationData = '{"email":"ccollazo@monmouth.edu","password":"mubaseball"}'

authenticationResponse = requests.post(
    'https://cloud.rapsodo.com/v2/auth/login', headers=authenticationHeaders, data=authenticationData)

JWT = authenticationResponse.json()['token']


pitchersHeaders = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://cloud.rapsodo.com/2.1/',
    'Origin': 'http://cloud.rapsodo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Authorization': JWT,
    'Sec-Fetch-Mode': 'cors',
    'Filter': '{"sport":2,"combine":1,"coaches":[1102083,1102645],"groups":[]}',
}

pitchersRespone = requests.get(
    'https://cloud.rapsodo.com/v2/pitching/team-players', headers=headers)

# print response.json()

# print str(response.json())

pitchersJSON = response.json()


print(json.dumps(pitchersJSON))


# GETS SESSIONS FOR specific player ID
sessionHeaders = {
    'Sec-Fetch-Mode': 'cors',
    'Origin': 'http://cloud.rapsodo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Filter': '{"sport":2,"combine":1,"coaches":[1102083,1102645],"groups":[]}',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://cloud.rapsodo.com/2.1/',
    'Authorization': JWT,
}

# begin date and end date, this grabs all
sessionPostData = '{"beginDate":0,"endDate":9999999999999,"player_id":101375,"player_type":"1"}'

sessionDataResponse = requests.post(
    'https://cloud.rapsodo.com/v2/player/allsessions', headers=headers, data=data)


print()
print()
print()
print()
print()

print(json.dumps(sessionDataResponse.json()))

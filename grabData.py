import requests
import json
import ast
import time
import csv
from datetime import datetime
import mysql.connector

# # ADD INTO SQL
mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="Monmouth2020",
    database="mubaseball"
)

mycursor = mydb.cursor()

# sql = "INSERT INTO `Pitch Type` (pitch_type, Description) VALUES (%s, %s)"
# val = (9, "test pitch")
# mycursor.execute(sql, val)
# mydb.commit()


# sessionSQL = "INSERT INTO captured_data (session_pitch_id, releaseHeight, horizontalBreak, spinClockTiltHour, date, szx, szy, selected, verticalBreak, _hour, videoPointerID, speed, no, Pitch_Type_pitchType, _minute, spinConfidence, spinEfficiency, releaseSide, trueSpin, _month, _milisecond, strike, _day, _year, pitch_id, spin, launchAngle, _second, spinAxis, releaseExtension, rifleSpin, gyroDegree, mode, Pitcher_pitcher_id, spinClockTiltMinute, horizontalAngle, memo, sessionID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# valSQL = (playerSessionFull[i]['session_pitch_id'], 123.4, 432.1, 111, '2019-09-27 00:00:00', 1.1, 2.2, 'sel', 3.3, 9, 'video', 69.0, 0, 0, 13, 5.5, 6.6, 7.7, 1000, 10, 9, 'Y', 15, 16, 35, 88, 8.8, 11, 'spin axes', 'relEx', 9.9, 45.0, 0, 101375, 77, 12.3, 'memo', 99)
# mycursor.execute(sessionSQL, valSQL)
# mydb.commit()


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

# print(JWT)

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
    'https://cloud.rapsodo.com/v2/pitching/team-players', headers=pitchersHeaders)

# print(pitchersRespone)

# write the ptchers.json file using the team-players response
with open('pitchers.json', 'w') as output:
    json.dump(pitchersRespone.json()['data'], output)

pitchersJSON = pitchersRespone.json()['data']
print(pitchersJSON)

# loop
playerIDs = []
for pitcher in pitchersJSON:
    playerIDs.append(str(pitcher['_id']))

startTime = time.time()

for id in playerIDs:

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

    
    # beginDate will always be today
    sessionPostData = '{"beginDate":0,"endDate":9999999999999,"player_id":' + \
        id + ',"player_type":"1"}'

    sessionDataResponse = requests.post(
        'https://cloud.rapsodo.com/v2/player/allsessions', headers=sessionHeaders, data=sessionPostData)

    # if pitcherNames[count].__contains__('Guest') == False:
    with open('sessions/' + id + '.json', 'w') as outfile:
        json.dump(sessionDataResponse.json()['data'], outfile)

endTime = time.time()

elapsedTime = int(endTime - startTime)

# took 66 seconds to execute and make all JSON
print("Time to make sessions JSONs: " + str(elapsedTime) + " seconds")


# create pitcherCSV
with open('pitchers.json') as f:
    pitcherData = json.load(f)

# get the keys for the header from the pitchers.json
keys = pitcherData[0].keys()
print(keys)
keys = list(keys)
keys.append('hitter_status')

# write the csv file using the pitcher data
with open('pitchers.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(pitcherData)


# create array of the dictionaries to hold each jsons dictionary
sessionDicts = []

sessionTableDicts = []

count = 0

sessionID = -1

# loop through IDs and grab each json and make dict of each and add to sessionDicts
for id in playerIDs:
    with open('sessions/' + id + '.json') as f:
        playerSessionFull = json.load(f)
        curDate = ''

        playerSession = []
        sessionDict = []

        for i in range(len(playerSessionFull)):

            # check that its valid id
            if len(playerSessionFull[i]['_id'].split('@')[0]) > 5:
                playerSessionFull[i]['_id'] = playerSessionFull[i]['_id'].split('@')[
                    0]
                playerSessionFull[i]['session_pitch_id'] = count
                playerSessionFull[i]['date'] = datetime.strptime(
                    playerSessionFull[i]['date'], '%d %b %y')

                if curDate != playerSessionFull[i]['date']:
                    sessionID = sessionID + 1
                    playerSessionFull[i]['sessionID'] = sessionID
                    curDate = playerSessionFull[i]['date']
                    sessionDict.append({'idSession': sessionID,
                                        'date': playerSessionFull[i]['date'], 'Pitcher__id': playerSessionFull[i]['_id']})
                else:
                    playerSessionFull[i]['sessionID'] = sessionID

                playerSession.append(playerSessionFull[i])

                count = count + 1

        sessionDicts.append(playerSession)
        sessionTableDicts.append(sessionDict)


# get keys for the sessions
keys = sessionDicts[0][0].keys()
keys = list(keys)
keys.append('memo')
# keys.append('session_pitch_id')

# write the csv for ALL sessions
with open('sessions.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    for session in sessionDicts:
        dict_writer.writerows(session)


keys = sessionTableDicts[0][0].keys()
with open('sessionTable.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    for session in sessionTableDicts:
        dict_writer.writerows(session)

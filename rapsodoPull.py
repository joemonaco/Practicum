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
    database="mubb"
)

mycursor = mydb.cursor()

# Delete all rows from captured_data and session
sql1 = "SET SQL_SAFE_UPDATES = 0;"
sql2 = "delete from captured_data;"
sql3 = "delete from session;"
mycursor.execute(sql1)
mycursor.execute(sql2)
mycursor.execute(sql3)

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
# print(pitchersJSON)

# loop
playerIDs = []
for pitcher in pitchersJSON:
    playerIDs.append(str(pitcher['_id']))

startTime = time.time()


curTime = int(round(time.time() * 1000))

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
    sessionPostData = '{"beginDate":0,"endDate":' + str(curTime) +',"player_id":' + \
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

                if playerSessionFull[i]['gyroDegree'] == '-':
                    playerSessionFull[i]['gyroDegree'] = 0
                if playerSessionFull[i]['releaseExtension'] == '-':
                    playerSessionFull[i]['releaseExtension'] = 0
                if playerSessionFull[i]['horizontalAngle'] == '-':
                    playerSessionFull[i]['horizontalAngle'] = 0
            
                playerSession.append(playerSessionFull[i])
                # print(playerSessionFull[i])
                count = count + 1
                sessionSQL = "INSERT INTO captured_data (session_pitch_id, releaseHeight, horizontalBreak, spinClockTiltHour, date, szx, szy, selected, verticalBreak, _hour, videoPointerID, speed, no, Pitch_Type_pitchType, _minute, spinConfidence, spinEfficiency, releaseSide, trueSpin, _month, _milisecond, strike, _day, _year, pitch_id, spin, launchAngle, _second, spinAxis, releaseExtension, rifleSpin, gyroDegree, mode, Pitcher_pitcher_id, spinClockTiltMinute, horizontalAngle, memo, sessionID) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                valSQL = (playerSessionFull[i]['session_pitch_id'], playerSessionFull[i]['releaseHeight'], playerSessionFull[i]['horizontalBreak'], playerSessionFull[i]['spinClockTiltHour'], playerSessionFull[i]['date'], playerSessionFull[i]['szx'], playerSessionFull[i]['szy'], playerSessionFull[i]['selected'],playerSessionFull[i]['verticalBreak'], playerSessionFull[i]['_hour'], playerSessionFull[i]['videoPointerID'], playerSessionFull[i]['speed'], playerSessionFull[i]['no'], playerSessionFull[i]['pitchType'], playerSessionFull[i]['_minute'], playerSessionFull[i]['spinConfidence'], playerSessionFull[i]['spinEfficiency'], playerSessionFull[i]['releaseSide'], playerSessionFull[i]['trueSpin'], playerSessionFull[i]['_month'], playerSessionFull[i]['_milisecond'], playerSessionFull[i]['strike'], playerSessionFull[i]['_day'], playerSessionFull[i]['_year'], playerSessionFull[i]['pitch_id'], playerSessionFull[i]['spin'], playerSessionFull[i]['launchAngle'], playerSessionFull[i]['_second'], playerSessionFull[i]['spinAxis'],playerSessionFull[i]['releaseExtension'], playerSessionFull[i]['rifleSpin'], playerSessionFull[i]['gyroDegree'], playerSessionFull[i]['mode'], playerSessionFull[i]['_id'], playerSessionFull[i]['spinClockTiltMinute'], playerSessionFull[i]['horizontalAngle'], 'memo', playerSessionFull[i]['sessionID'])
                mycursor.execute(sessionSQL, valSQL)
                mydb.commit()
        # print(sessionDict[0])
        sessionDicts.append(playerSession)
        sessionTableDicts.append(sessionDict)

        for session in sessionDict:
            sessionTableSQL = "INSERT INTO session (idSession, date, Pitcher__id) VALUES (%s, %s, %s)"
            valTableSQL = (session['idSession'], session['date'], session['Pitcher__id'])
            mycursor.execute(sessionTableSQL, valTableSQL)
            mydb.commit()

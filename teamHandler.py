import requests

from pynput import keyboard
import keyboard as kb
import time

class TeamHandler:
    teamEnums = {}
    timesToIgnore = 0

    def __init__(self):
        self.teamEnums = self.assembleEnums()

    def procRequest(self, req:str):
        try:
            infor = requests.get(req, verify=False).json()
            return infor
        except requests.exceptions.RequestException:
            print("Try launching a game first!")
            return None

    def assembleEnums(self):
        selfTeam = self.getTeamMates(self.getSelfTeam())
        tempEnums = {}
        for idx, i in enumerate(selfTeam):
            tempEnums[idx] = i['summonerName']
        return tempEnums

    def getSelf(self):
        self = self.procRequest('https://127.0.0.1:2999/liveclientdata/allgamedata')
        selfTeam = [x for x in self['allPlayers'] if x['summonerName'] == self['activePlayer']['summonerName']][0]['team']
        self['team'] = selfTeam
        return self

    def getSelfTeam(self):
        selfTeam = self.getSelf()['team']
        return selfTeam

    def getTeam(self):
        team = self.procRequest('https://127.0.0.1:2999/liveclientdata/playerlist')
        return team

    def getTeamMates(self, selfTeam:str):
        tempTeamMates = []
        for player in self.getTeam():
            if player['team'] == selfTeam:
                tempTeamMates.append(player)
        return tempTeamMates

    def retrieveLiveStatus(self, ID):
        team = self.getTeam()
        allySummName = self.teamEnums[ID]
        ally = [x for x in team if x['summonerName'] == allySummName][0]
        returnMsg = ''
        if ally['isDead']:
            returnMsg = f'{ally["championName"]} - Respawning in {round(ally["respawnTimer"])}s.'
        else:
            returnMsg = f'{ally["championName"]} - Alive.'
        return returnMsg
    
    def autoGUISending(self, ID, VALID_KEYS_AS_CHARS):
        if self.timesToIgnore > 0:
            self.timesToIgnore -= 1
            if self.timesToIgnore < 0:
                self.timesToIgnore = 0
                print("This should not have happened!")
            return self.timesToIgnore
        msg = self.retrieveLiveStatus(ID)
        timesToIgnore = 0
        for c in msg:
            if c in VALID_KEYS_AS_CHARS:
                timesToIgnore += 1
        kb.send('backspace')
        kb.send('delete')
        kb.write(msg)
        kb.send('enter')
        time.sleep(0.001)
        kb.send('enter')
        self.timesToIgnore += timesToIgnore
        return timesToIgnore

# force remove key from set that isn't modifier key upon guisending
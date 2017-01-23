import sys
import requests
from StringIO import StringIO
import codecs
import json
import io
import csv
import MySQLdb


db = MySQLdb.connect()  
cursor = db.cursor()


data_all = []

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------      
allteamslug_dup = ["flash-wolves","g2-esports","supermassive-esports"]

allteamslug = []
for item in allteamslug_dup:
    if item not in allteamslug:
        allteamslug.append(item)
print len(allteamslug)

alltournamentslug_dup = ["69298c0c-16ae-490a-8e9c-cfe4620a6bfb"]

alltournamentslug = []
for item in alltournamentslug_dup:
    if item not in alltournamentslug:
        alltournamentslug.append(item)
print len(alltournamentslug)

alltournamentslug
count3 = 0
error_came_in = []                  
for count1 in alltournamentslug:  
    for count2 in allteamslug: 
        try: 
            url = "&tournament=" + str(count1)
            r = requests.get(url)
            json_data = json.loads(r.content)
            data_complete = json_data

            try:
                highlanderTournaments = data_complete['highlanderTournaments']
            except:
                highlanderTournaments = None
                sql = "INSERT INTO `highlanderTournaments` (`url`) VALUES("+'"'+ url + '"'+")"
                cursor.execute(sql)
            try:
                players = data_complete['players']
            except:
                players = None
                sql = "INSERT INTO `players` (`url`) VALUES("+'"'+ url + '"'+")"
                cursor.execute(sql)
            try:
                scheduleItems = data_complete['scheduleItems']
            except:
                scheduleItems = None
                sql = "INSERT INTO `scheduleItems` (`url`) VALUES("+'"'+ url + '"'+")"
                cursor.execute(sql)
            try:
                teamRosterStats = data_complete['teamRosterStats']
            except:
                teamRosterStats = None
                sql = "INSERT INTO `teamRosterStats` (`url`) VALUES("+'"'+ url + '"'+")"
                print "sql : " + sql
                cursor.execute(sql)
            try:
                teams = data_complete['teams']
            except:
                teams = None
                sql = "INSERT INTO `teams` (`url`) VALUES("+'"'+ url + '"'+")"
                cursor.execute(sql)
            try:
                teamStatsHistories = data_complete['teamStatsHistories']
            except:
                teamStatsHistories = None
                sql = "INSERT INTO `teamStatsHistories` (`url`) VALUES("+'"'+ url + '"'+")"
                cursor.execute(sql)
            try:
                teamStatsSummaries = data_complete['teamStatsSummaries']
            except:
                teamStatsSummaries = None   
                sql = "INSERT INTO `teamStatsSummaries` (`url`) VALUES("+'"'+ url + '"'+")"
                cursor.execute(sql)
    
    #------------------------highlanderTournaments----------------------------------
            if highlanderTournaments != None: 
                highlanderTournaments_data = []
                for item in highlanderTournaments:
                    tmp = []
                    try:
                        a = item['id'] #ht_id
                    except:
                        a = "id not found"        
                    try:
                        b = item['title']
                    except:
                        b = "title not found"
                    try:
                        c = item['description']
                    except:
                        c = "description not found"
                    try:
                        d = item['leagueReference']
                    except:
                        d = "leagueReference not found"
                    try:
                        e = item['roles']
                    except:
                        e = "roles not found"
                    try:
                        f = item['matchType']
                    except:
                        f = "matchType not found"
                    try:
                        g = item['gameMode']
                    except:
                        g = "gameMode not found"
                    try:
                        h = item['rosteringStrategy']
                    except:
                        h = "rosteringStrategy not found"
                    try:
                        i = item['queues']
                    except:
                        i = "queues not found"
                    try:
                        j = item['rosters']
                    except:
                        j = "rosters not found"    
                    try:
                        k = item['published']
                    except: 
                        k = "published not found"
                    try:
                        l = item['breakpoints']    
                    except: 
                        l = "breakpoints not found"
                    try:
                        m = item['brackets']
                    except:
                        m = "brackets not found"
                    try:
                        n = item['standings']
                    except:
                        n = "standings not found"
                    try:
                        o = item['liveMatches']
                    except:
                        o = "liveMatches not found"
                    try:
                        p = item['startDate']
                    except:
                        p = "startDate not found"
                    try:
                        q = item['endDate']
                    except:
                        q = "endDate not found"
                    try:
                        r = item['platformIds']
                    except:
                        r = "platformIds not found"    
                    try:
                        s = item['gameIds']    
                    except:
                        s = "gameIds not found"
                    try:
                        t = item['league'] 
                    except:
                        t = "league not found"
                    
                    tmp.append(str(a).encode('utf-8').replace("'","").replace('"',''))
                    tmp.append(str(b).encode('utf-8').replace("'","").replace('"',''))

                    highlanderTournaments_data.append(tmp)
                    sql_command1 = "INSERT INTO highlanderTournaments VALUES();"
                    print sql_command1
                    cursor.execute(sql_command1)
    
        #------------------------players------------------------------------------------
                if players != None:
                    players_data = []
                    for item in players: 
                        
                        tmp = []
                        try:
                            a = item['id'] #players_id
                        except:
                            a = "id not found"
                        try:
                            b = item['slug']
                        except:
                            b = "slug not found"
                        try:
                            c = item['name']
                        except:
                            c = "name not found"
                        try:
                            d = item['firstName']
                        except:
                            d = "firstName not found"
                        try:
                            e = item['lastName']
                        except:
                            e = "lastName not found" 
                        try:
                            f = item['roleSlug']
                        except:
                            f = "roleSlug not found" 
                        try:
                            g = item['photoUrl']
                        except:
                            g = "photoUrl not found"
                        try:
                            h = item['hometown']
                        except:
                            h = "hometown not found"
                        try:
                            i = item['region']
                        except:
                            i = "region not found"
                        try:
                            j = item['birthdate']
                        except:
                            j = "birthdate not found"
                        try:
                            k = item['createdAt']
                        except:
                            k = "createdAt not found"
                        try:
                            l = item['updatedAt']
                        except:
                            l = "updatedAt not found"
                        try:
                            m = item['bios']
                        except:
                            m = "bios not found"
                        try:
                            n = item['foreignIds']
                        except:
                            n = "foreignIds not found"
                        try:
                            o = item['socialNetworks']
                        except:
                            o = "socialNetworks not found"
                        try:
                            p = item['champions']
                        except:
                            p = "champions not found"    
                        
                        tmp.append(str(a).encode('utf-8').replace("'","").replace('"',''))
  
                        #print tmp
                        players_data.append(tmp)
                        try:
                            sql_command2 = "INSERT INTO players VALUES(" ");"
                            print sql_command2
                            cursor.execute(sql_command2)  
                        except:
                            sql_command2 = "INSERT INTO `players` (`url`) VALUES("+'"'+ url + '"'+")"   
                            cursor.execute(sql_command2)           
    
        #------------------------scheduleItems-----------------------------------------------
                    if scheduleItems != None:
                        scheduleItems_data = []
                        for item in scheduleItems: 
                            
                            tmp = []
                            try:
                                a = item['id'] #id_scheduleItems
                            except:
                                a = "id not found"
                            try:
                                b = item['content']
                            except:
                                b = "content not found"
                            try:
                                c = item['scheduledTime']
                            except:
                                c = "scheduledTime not found"
                            try:
                                d = item['tags']
                            except:
                                d = "tags not found"
                            try:
                                e = item['match']  #match_scheduleItems
                            except:
                                e = "match not found" 
                            try:
                                f = item['tournament']
                            except:
                                f = "tournament not found" 
                            try:
                                g = item['bracket']
                            except:
                                g = "bracket not found"
                            try:
                                h = item['league']
                            except:
                                h = "league not found"
        
                        tmp.append(str(a).encode('utf-8').replace("'","").replace('"',''))
                        tmp.append((h).replace("'","").replace('"',''))
                        scheduleItems_data.append(tmp)
                        sql_command3 = "INSERT INTO scheduleItems VALUES(" ");"
                        print sql_command3
                        cursor.execute(sql_command3)                
    
        #------------------------teamRosterStats-----------------------------------------------
                    if teamRosterStats != None:
                        teamRosterStats_data = []
                        for item in teamRosterStats: 
                            
                            tmp = []
                            try:
                                a = item['playerid'] #id_scheduleItems
                            except:
                                a = "playerid not found"
                            try:
                                b = item['gamesPlayed']
                            except:
                                b = "averageAssists not found"
                            try:
                                c = item['averageAssists']
                            except:
                                c = "averageAssists not found"
                            try:
                                d = item['averageDeaths']
                            except:
                                d = "averageDeaths not found"
                            try:
                                e = item['averageKillParticipation']  #match_scheduleItems
                            except:
                                e = "averageKillParticipation not found" 
                            try:
                                f = item['averageKills']
                            except:
                                f = "averageKills not found" 
                            try:
                                g = item['summonerName']
                            except:
                                g = "summonerName not found"
                            try:
                                h = item['championIds']
                            except:
                                h = "championIds not found"
        
                        tmp.append(str(a).encode('utf-8').replace("'","")
                        cursor.execute(sql_command4)             
    
        except:
            error_came_in.append(url)
            pass


f = open("error_came_in_url", "w")
f.write("\n".join(map(lambda x: str(x), error_came_in)))  
f.close()

db.commit()
cursor.close()
    

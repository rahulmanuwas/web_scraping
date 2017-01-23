# !/usr/bin/python

import csv
import requests
from bs4 import BeautifulSoup

import MySQLdb
db = MySQLdb.connect()        
                     
# prepare a cursor object using cursor() method
cursor = db.cursor()

#Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS TABLEX;")


sql = """CREATE TABLE IF NOT EXISTS TABLEX (
         SKIN_QUALITY  VARCHAR(500),
         PRICE  VARCHAR(50),
         LISTINGS VARCHAR(50),  
         MEDIAN VARCHAR(50),
         VOLUME VARCHAR(50),
         BITSKIN VARCHAR(50),
         OPSKIN VARCHAR(50),
         KEYS_1  VARCHAR(50),
         NAME VARCHAR(500),
         URL VARCHAR(500)
         );"""

cursor.execute(sql)                     

# Rewrite the file from the beginning
with open('pagelinks_all') as f:
    urlarray = []
    for line in f:
        urlarray.append(line) 
        
print "Total links found:" + str(len(urlarray))

with open('table_all.csv','w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows('')
fp.close()

for i in range (len(urlarray)):
    print "Writing Table : " + str(i)
    url= urlarray[i].replace("\n", "") 

    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.content,'html.parser')
    
    table = soup.find_all("table")    
    tbody = table[0].find("tbody")
    table_rowh = tbody.find_all("tr")
    
    # Weapon Name and URL
    weapon= url.split("/")
    weapon_name = weapon[5]
    print weapon_name 
    k= weapon_name.replace("\n", "") #"Weapon Name : " + weapon_name
    l= url.replace("\n", "")  #"Weapon URL : " + url
    
    table_complete = []
    
    for item in table_rowh:
        tmp = []
        table_rowd = item.find_all("td")
        cnt = 0
        for rows in table_rowd:
            tmp.append((table_rowd[cnt].text.encode('utf-8').replace("u","").replace("\t","").replace("\xe2\x82\xb9","").replace("," ,"").replace("\n","")))            
            cnt = cnt + 1
        print "count:" + str(cnt)
        tmp.append(k)
        tmp.append(l)
        table_complete.append(tmp)
     
        try:
            sql_command = "INSERT INTO TABLEX VALUES(" + "'"+tmp[0]+"'" + ',' + "'"+tmp[1]+"'" + ',' + "'"+tmp[2]+"'" + ',' + "'"+tmp[3]+"'" + ',' + "'"+tmp[4]+"'" + ',' + "'"+tmp[5]+"'" + ',' + "'"+tmp[6]+"'" + ',' + "'"+tmp[7]+"'" + ',' + "'"+tmp[8]+"'" + ',' + "'"+tmp[9]+"'" +  ");"        
            print sql_command
            cursor.execute(sql_command)
            db.commit()
        except:
            pass         
    
    with open('table_all.csv','a') as fp:
        a = csv.writer(fp, delimiter=',')
        for lists in table_complete:
            data = table_complete
        a.writerows(data)
        
fp.close()
db.close()
                

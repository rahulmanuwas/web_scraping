from bs4 import BeautifulSoup
import urllib2
from subprocess import call
import datetime
import re
import requests, pprint
import time
import MySQLdb
import hashlib
import json
import csv
from datetime import date
from dateutil.relativedelta import relativedelta

conn = MySQLdb.connect()

def getSchemeDetails(mfID, scID):
    url = ""

    params = {'strMfID':mfID, 'strScID':scID}
    r = requests.post(url, params=params)

    print r.status_code
    #print r.content
    if "No records to display" in r.content:
        print "No records to display"
        return
    soup = BeautifulSoup(r.content, 'html.parser')
    print soup.prettify()

    headers = soup.findAll("h3")
    texts = soup.findAll("p")
    data_dict = {}
    key = []
    value = []
    new_txt = str(mfID) + str(scID)
    data_dict['uniqu']= hashlib.md5(new_txt).hexdigest()
    data_dict['mfID']  = mfID
    data_dict['scID']  = scID

    for i in range(len(headers)):
        key = headers[i].text.encode('utf-8')
        value = texts[i].text.encode('utf-8')
        print key, value
        key = key.replace(" ", "_")
        data_dict[key] = value


    texts = soup.find("a")
    if texts != None:
        print texts['href']
        data_dict["document_url"] = texts['href'].encode("UTF-8")

    print data_dict

    placeholders = ', '.join(['%s'] * len(data_dict))
    columns = ', '.join(data_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("scheme_info", columns, placeholders)
    x = conn.cursor()
    try:
        x.execute(sql, data_dict.values())
        print "inserted"
        conn.commit()
    except:
        print "dsdsfgd"
        print(x._last_executed)
        conn.rollback()
    x.close()

def getFundSchemeId():
    cursor = conn.cursor()
    cursor.execute("SELECT scheme_id, fund_id FROM  `schemes` where id < 28357 order by id desc")
    brands = cursor.fetchall()
    cursor.close()
    return brands

for row in getFundSchemeId():
    scheme_id = row[0]
    print scheme_id[2:]
    fund_id = row[1]
    print fund_id
    getSchemeDetails(fund_id, scheme_id[2:])
    time.sleep(2)

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

conn = MySQLdb.connect(host= "localhost", user="", passwd="", db=" ")

def getHistoryData(mfID, scID):
    url = " "
    for i in range(1,300):
        print i
        toDate = date.today() + relativedelta(months=-i+1)
        toDate = toDate.strftime('%d-%b-%Y')
        six_months = date.today() + relativedelta(months=-i)
        six_months = six_months.strftime('%d-%b-%Y')

        params = {'ID' :53}
        r = requests.post(url, params=params)

        print r.status_code
        print r.content
        if "No records to display" in r.content and i == 2:
            print "No records to display"
            return
        soup = BeautifulSoup(r.content, 'html.parser')
        trs = soup.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td")
            print tds
            tmp = {}
            if tds != None and len(tds) > 3:
                new_txt = str(mfID) + str(scID) + tds[3].text
                tmp['uniqu']= hashlib.md5(new_txt).hexdigest()
                tmp['Net_Asset_Value'] = tds[0].text
                tmp['Repurchase_Price'] = tds[1].text
                tmp['Sale_Price'] = tds[2].text
                tmp['NAV_date'] = tds[3].text

                tmp['mfID']  = mfID
                tmp['scID']  = scID
                tmp['fDate'] = six_months
                tmp['tDate'] = toDate
                placeholders = ', '.join(['%s'] * len(tmp))
                columns = ', '.join(tmp.keys())
                sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("scheme_date", columns, placeholders)
                x = conn.cursor()
                try:
                    x.execute(sql, tmp.values())
                    print "inserted"
                    conn.commit()
                except:
                    print "dsdsfgd"
                    print(x._last_executed)
                    conn.rollback()
                x.close()

def getFundSchemeId():
    cursor = conn.cursor()
    cursor.execute("SELECT scheme_id, fund_id FROM  `schemes` order by id desc")
    brands = cursor.fetchall()
    cursor.close()
    return brands

def getFundsId():
    cursor = conn.cursor()
    cursor.execute("SELECT fund_id, id FROM  `Mutual_Fund`")
    brands = cursor.fetchall()
    cursor.close()
    return brands

def getSchemes(fund_id):
    url = "https://www.amfiindia.com/modules/NavHistorySchemeNav"
    params = {'ID' : 1}
    payload = json.dumps(params)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept":"*/*", "Host": "www.amfiindia.com", "Cache-Control": "no-cache", "X-Requested-With": "XMLHttpRequest"}
    #headers = json.dumps(headers)
    r = requests.post(url, {'ID' : fund_id}, headers=headers)
    print r.status_code
    resp = r.json()
    x = conn.cursor()
    for item in resp:
        print item['Text']
        try:
            x.execute("INSERT INTO schemes VALUES (%s,%s,%s)",(item['Text'], item['Value'], fund_id))
            print "inserted"
            conn.commit()
        except:
            print "dsdsfgd"
            print(x._last_executed)

    x.close()


for row in getFundSchemeId():
    scheme_id = row[0]
    print scheme_id
    fund_id = row[1]
    print fund_id
    getHistoryData(fund_id, scheme_id)
    time.sleep(2)

#getHistoryData(9, 102000)

conn.close()

from bs4 import BeautifulSoup
from subprocess import call
from datetime import date
import requests
import base64
import random
import time
import sys
import os
import random 
from os import listdir,path
from os.path import isfile, join
import json
from requests.auth import HTTPProxyAuth
import csv
import MySQLdb
import cjson
import re
import hashlib
from dateutil.parser import parse


connection = MySQLdb.connect()
cursor = connection.cursor()

connection2 = MySQLdb.connect()
cursor2 = connection2.cursor()
cursor2.execute ("SELECT `ITEMS_TO_RESPOND`, `url` FROM `open_opportunity`")
data = cursor2.fetchall ()
cursor2.close()
connection2.close()

json_data_encode = []
count = 1
for row in data :
    if row[0] != "":
        if row[0] != "Items to respond not found.":
            try:  
                print "count = " + str(count)    
                #print row
                count = count +1 
                k = row[1].encode('utf-8') #url
            #-------------------------------------- items to respond ------------------------------------------
                j = row[0].encode('utf-8')
                #print j 
                a = re.split('},', j, flags=re.IGNORECASE) 
                i = 0
                for i in range (len(a)):
                    a[i] = a[i].replace("[","").replace("]","")
                    if "}" not in a[i]:
                        a[i] = a[i] + "}"
                        #print a[0]
                    try:
                       dict_contact = json.loads(a[i].encode('utf-8').replace("'",'"').replace("\t","").replace("\n",""))
                    except:
                        dict_contact = cjson.encode(a[i].replace("'",'"').replace("\n","").replace("\t","")) #overview                
                    #print dict_contact  
                   
                    try:
                        # Unit_of_Measurement
                        b1 = dict_contact['Unit_of_Measurement']
                        #print b1
                    except:
                        b1 = ""
                    
                    try:
                        # Delivery Terms
                        b2 = dict_contact['Delivery Terms']
                        #print b2
                    except:
                        b2 = ""
                    
                    try:
                        # Delivery Date'
                        b3 = dict_contact['Delivery Date']
                        b3 = str(parse(b3))
                        #print b3
                    except:
                        b3 = ""            
                    
                    try:
                        # Title
                        b4 = dict_contact['Title']
                        #print b4
                    except:
                        b4 = ""
                   
                    try:
                        # Required_Quantity
                        b5 = dict_contact['Required_Quantity']
                        #print b5
                    except:
                        b5 = ""
                   
                    try:
                        # Location
                        b6 = dict_contact['Location']
                        #print b6
                    except:
                        b6 = ""
                    
                    try:
                        # Remarks
                        b7 = dict_contact['Remarks']
                        #print b7
                    except:
                        b7 = ""
                   
                    try:
                        # Quantity
                        b8 = dict_contact['Quantity']
                        #print b8
                    except:
                        b8 = ""
                   
                    #print b1, b2, b3, b4, b5, b6, b7, b8
                    
                    url = k
                    try:
                        cursor.execute("SELECT `id` FROM `open_tenders` where `quotation_no` like" + "'"+ tender_no +"'" )
                        id_value = cursor.fetchall()
                        print "id_value = "
                        print id_value[0][0]
                        tender_id = id_value[0][0]
                    except:
                        try:
                            cursor.execute("SELECT `id` FROM `open_tenders` where `tender_no` like" + "'"+ tender_no +"'" )
                            id_value = cursor.fetchall()
                            print "id_value = "
                            print id_value[0][0]
                            tender_id = id_value[0][0]
                        except:
                            tender_id = None
                    
                    

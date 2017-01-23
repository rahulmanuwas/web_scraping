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

connection = MySQLdb.connect(host= "localhost", user="", passwd="", db="")
cursor = connection.cursor()



# ----------------connect with gebiz database -----------------------------------------------------
connection2 = MySQLdb.connect(host= "localhost", user="", passwd="", db="")
cursor2 = connection2.cursor()
cursor2.execute ("SELECT `WHO_TO_CONTACT`, `WHO_TO_CONTACT1`, `url` FROM `close_opportunity`")
data = cursor2.fetchall ()
cursor2.close()
connection2.close()

# print the rows
json_data_encode = []
count = 1
for row in data :
    print "count = " + str(count)    
    #print row
    count = count +1 
    l = row[0].replace("\n","") #who_to_contact               
    m = row[1].encode('utf-8')
    n = row[2]
#-------------------------------------- who to contact ------------------------------------------
    #print l    
    except_string = [".pdf", ".doc", "annex", "secondary contact not found", "contract", "document", "quotation", "specification", "doc a", "tender", "agreement", "terms", "schedule", ".zip"]
    check_status1 = 0
    for item in except_string:
        if item in (str(l).lower()):
            check_status1 = 1
    if check_status1 == 0:      
        a = re.split(',', l, flags=re.IGNORECASE)
        dict_contact = {}
        for item in a:    
            b = re.split(',', item, flags=re.IGNORECASE)
            c = re.split(':', b[0], flags=re.IGNORECASE) 
            try:    
                key = c[0].replace("'","").replace("[","").replace("]","")
                value = c[1].replace("'","").replace("[","").replace("]","")    
                dict_contact[key] = value            
            except:
                pass
        #print dict_contact
        
        try:
            # Primary Contact
            b1 = dict_contact['Primary Contact']
            #print b1
        except:
            b1 = ""
        try:
            # email
            b2 = dict_contact[' email']
            b2 = b2.replace(" ","")
            #print b2
        except:
            b2 = ""        
        try:
            # Phone 1
            b3 = dict_contact[' Phone 1']
            b3 = b3.replace(" ","")
            #print b3
        except:
            b3 = ""
        try:
            # Phone 2
            b4 = dict_contact[' Phone 2']
            b4 = b4.replace(" ","")
            #print b4
        except:
            b4 = ""
        try:
            # Address
            b5 = dict_contact[' Address']
            if b5 == b2: #if address is same as email 
                b5 = ""
            #print b5
        except:
            b5 = ""
        
        if "@" not in str(b2.lower()): #if email is not found and has been added to phone
                    tmp1 = b2
                    tmp2 = b3
                    b2 = ""
                    b3 = tmp1
                    b4 = tmp2 
        
        #print b1, b2, b3, b4, b5
#-------------------------------------- who to contact 1------------------------------------------   
    #print m
    try:
        except_string = [".pdf", ".doc", "annex", "secondary contact not found", "contract", "document", "quotation", "specification", "doc a", "tender", "agreement", "terms", "schedule", ".zip"]
        check_status2 = 0
        for item in except_string:
            if item in (str(m).lower()):
                check_status2 = 1
        if check_status2 == 0:        
            aa = re.split(',', m, flags=re.IGNORECASE)
            if len(aa) > 2:            
                dict_contact = {}
                for item in aa:    
                    b = re.split(',', item, flags=re.IGNORECASE)
                    c = re.split(':', b[0], flags=re.IGNORECASE) 
                    try:    
                        key = c[0].replace("'","").replace("[","").replace("]","")
                        value = c[1].replace("'","").replace("[","").replace("]","")    
                        dict_contact[key] = value            
                    except:
                        pass
                                        
                try:
                    # Primary Contact
                    bb1 = dict_contact['Secondary Contact']
                    #print bb1
                except:
                    bb1 = ""
                try:
                    # email
                    bb2 = dict_contact[' email']
                    bb2 = bb2.replace(" ","")
                    #print bb2
                except:
                    bb2 = ""        
                try:
                    # Phone 1
                    bb3 = dict_contact[' Phone 1']
                    bb3 = bb3.replace(" ","")
                    #print bb3
                except:
                    bb3 = ""
                try:
                    # Phone 2
                    bb4 = dict_contact[' Phone 2']
                    bb4 = bb4.replace(" ","")
                    #print bb4
                except:
                    bb4 = ""
                try:
                    # Address
                    bb5 = dict_contact[' Address']
                    #print bb5
                except:
                    bb5 = ""
                
                if "@" not in str(bb2): #if email is not found and has been added to phone
                    tmp1 = bb2
                    tmp2 = bb3
                    bb2 = ""
                    bb3 = tmp1
                    bb4 = tmp2        
                
                #print bb1, bb2, bb3, bb4, bb5 
    except:
        bb1 = bb2 = bb3 = bb4 = bb5 = ""
        #print bb1, bb2, bb3, bb4, bb5

#-------------------------------------- tender_no ------------------------------------------
    tender_no = n.replace("&status=AWARDED&type=TT&OPPORTUNITY_ID=0&origin=rss","").replace("https://www.gebiz.gov.sg/ptn/opportunityportal/opportunityDetails.xhtml?code=","").replace("&status=AWARDED&type=TQ&OPPORTUNITY_ID=0&origin=rss","").replace("&status=RELEASED&type=TT&OPPORTUNITY_ID=0&origin=rss","").replace("&status=RELEASED&type=TQ&OPPORTUNITY_ID=0&origin=rss","")    
    
#----------------------To fetch agency_id -------------------------------------------------------------------------------------------------------------------------------------------------
    try:
        cursor.execute("SELECT `id` FROM `closed_tenders` where `quotation_no` like" + "'"+ tender_no +"'" )
        id_value = cursor.fetchall()
        #print "tender_id_value = "
        #print id_value[0][0]
        tender_id = id_value[0][0]
    except:
        try:
            cursor.execute("SELECT `id` FROM `closed_tenders` where `tender_no` like" + "'"+ tender_no +"'" )
            id_value = cursor.fetchall()
            #print "tender_id_value = "
            #print id_value[0][0]
            tender_id = id_value[0][0]
        except:
            tender_id = None
    
    try:
        cursor.execute("SELECT `agency_id` FROM `closed_tenders` where `id` like" + "'"+ str(tender_id) +"'" )
        id_value2 = cursor.fetchall()
        #print "agency_id_value = "
        #print id_value2[0][0]
        agency_id = id_value2[0][0]
    except:
        print  "agency_id_value not found "
    
    
    try:
        try:
            if b1 != None: 
                sql_command = "INSERT INTO `contacts`(`agency_id`, `name`, `email`, `phone1`, `phone2`, `address`) VALUES ("+ "'"+str(agency_id)+"'" + ',' + "'"+b1+"'" + ',' + "'"+b2+"'" + ',' + "'"+b3+"'" + ',' + "'"+b4+"'" + ',' + "'"+b5+"'" +")"              
                #print sql_command
                cursor.execute(sql_command)
                connection.commit()
                
                contact_id = cursor.lastrowid
                #print "contact_id = " 
                #print contact_id   
                sql_command = "INSERT INTO `closed_tender_contacts`(`agency_id`, `tender_id`, `contact_id`) VALUES ("+ "'"+str(agency_id)+"'" + ',' + "'"+str(tender_id)+"'" + ',' + "'"+str(contact_id)+"'" +")"              
                #print sql_command
                cursor.execute(sql_command)
                connection.commit()
        except:
            try:
                if b1 != None: 
                    sql_command = "SELECT `id` FROM `contacts` WHERE `email` LIKE "+ "'"+str(b2)+"'" +" AND `phone1` LIKE "+ "'"+str(b3)+"'" +" AND `phone2` LIKE "+ "'"+str(b4)+"'"               
                    print sql_command
                    cursor.execute(sql_command)
                    id_value = cursor.fetchall()
                    contact_id = id_value[0][0]
                    print "contact_id = " 
                    print contact_id   
                    sql_command = "INSERT INTO `closed_tender_contacts`(`agency_id`, `tender_id`, `contact_id`) VALUES ("+ "'"+str(agency_id)+"'" + ',' + "'"+str(tender_id)+"'" + ',' + "'"+str(contact_id)+"'" +")"              
                    #print sql_command
                    cursor.execute(sql_command)
                    connection.commit()
            except:
                pass    
                    
                
        try:
            if bb1 != None:
                sql_command = "INSERT INTO `contacts`(`agency_id`, `name`, `email`, `phone1`, `phone2`, `address`) VALUES ("+ "'"+str(agency_id)+"'" + ',' + "'"+bb1+"'" + ',' + "'"+bb2+"'" + ',' + "'"+bb3+"'" + ',' + "'"+bb4+"'" + ',' + "'"+bb5+"'" +")" 
                #print sql_command
                cursor.execute(sql_command)
                connection.commit()
            
                contact_id = cursor.lastrowid   
                sql_command = "INSERT INTO `closed_tender_contacts`(`agency_id`, `tender_id`, `contact_id`) VALUES ("+ "'"+str(agency_id)+"'" + ',' + "'"+str(tender_id)+"'" + ',' + "'"+str(contact_id)+"'" +")"              
                #print sql_command
                cursor.execute(sql_command)
                connection.commit()
    
        except:
            try:
                if bb1 != None:
                    sql_command = "SELECT `id` FROM `contacts` WHERE `email` LIKE "+ "'"+str(bb2)+"'" +" AND `phone1` LIKE "+ "'"+str(bb3)+"'" +" AND `phone2` LIKE "+ "'"+str(bb4)+"'"              
                    print sql_command
                    cursor.execute(sql_command)
                    id_value = cursor.fetchall()
                    contact_id = id_value[0][0]
                    print "contact_id = " 
                    print contact_id    
                    sql_command = "INSERT INTO `closed_tender_contacts`(`agency_id`, `tender_id`, `contact_id`) VALUES ("+ "'"+str(agency_id)+"'" + ',' + "'"+str(tender_id)+"'" + ',' + "'"+str(contact_id)+"'" +")"              
                    #print sql_command
                    cursor.execute(sql_command)
                    connection.commit() 
            except:
                pass
                
    except:
        print "Error found!"
    
#------------------------------------------------------------------------------------------------------------------------

# close the cursor object
cursor.close ()

# close the connection
connection.close ()

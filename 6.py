from bs4 import BeautifulSoup
import urllib2
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
import hashlib
import redis
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1024, 768))
display.start()

#pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
#r = redis.Redis(connection_pool=pool)

def init_driver():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.wait = WebDriverWait(driver, 5)
    return driver

#-----------------------------------------------------------------------------------

count1 = 0
urlarray = []


with open('/home/rahulmanuwas/all_closed_quotations') as f:
    urlarray = []
    url_array2 = []
    for line in f:
        if line != "" :
            if line not in url_array2:
                xyz_url = "https://www.gebiz.gov.sg/ptn/opportunityportal/opportunityDetails.xhtml?code=" + str(line.replace("\n",""))
                urlarray.append(xyz_url)
                url_array2.append(line) 
print "Searching for links in " + str(len(urlarray)) + " urls...."


def getKeys(overview_table_key):
    key_array = []
    for item in overview_table_key:
        if(item == "GRA Supply/Work Heads [Tendering Capacity]"):
            key_array.append("GRA_Supply")
        if(item == "Tender No."):
            key_array.append("Tender_No")

def lookup(driver, query):    
    print "url : " + url
    driver.implicitly_wait(1)
    driver.get(url)
    time.sleep(0.3)
    driver.implicitly_wait(1)
    
    if (time.time() - start > 40):
        return
    
    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')
    
    main_div = soup.find("div", {"class": "formTabBar_MAIN"})
    inner_div = main_div.find("table", {"class", "formContainer_TABLE"})
    contect_div = inner_div.findAll("table", {"class", "formColumns_ROW-TABLE"})
# ----------------------------------------------------------------------------------------------------------------------
    k = len(contect_div) #Total Contect_div 
    print "Total div: " + str(k)
    
    #--------------Section Headings----------------------------------------------------
    section_headings = []
    for rows in inner_div:
        try:
            headers = inner_div.findAll("div", {"class":"formSectionHeader1_TEXT"})                
        except:
            pass
    for rows in headers:
        section_headings.append(rows.text.encode('utf-8'))
    
    i=0
    while i<3:  
        trs = contect_div[i].findAll("table", { "class" : "form2_ROW-TABLE" })
        gra = contect_div[i].findAll("table", { "class" : "formContainer_TABLE"})
        if gra != []:
            #print "i = " + str(i)
            break
        i = i+1
        
    overview_table = []
    
    #GRA text
    overview_table_key = []
    overview_data = {}
    if(len(gra) >= 2):
        gra = gra[i]
        try:
            lable = gra.find("div", {"class": "form2_ROW-LABEL"})
            lable = lable.find("span")            
            GRA_text = gra.find("span",{"class":"outputText_DESCRIPTION-GRAY"})
            GRA_append = GRA_text.text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
            overview_data[lable.contents[0].encode('utf-8').replace("\n","").replace("'","").replace('"','')] = GRA_append
        except:
            pass                
        try:
            lable = gra.find("div", {"class": "form2_ROW-LABEL"})
            lable = lable.find("span")
            GRA_text = gra.find("div",{"class":"formOutputText_VALUE-DIV"})
            GRA_append = GRA_text.text.encode('utf-8')
            overview_data[lable.contents[0].encode('utf-8').replace("\n","").replace("'","").replace('"','')] = overview_data[lable.contents[0].encode('utf-8').replace("\n","").replace("'","").replace('"','')] + " " + GRA_append
        except:
            pass
                    
    ## ---------------- Tender Details -----------------------------------------
    for tr in trs:
        tmp = []
        lable = tr.find("div", {"class": "form2_ROW-LABEL"})
        value = tr.find("div", {"class": "formOutputText_VALUE-DIV"})
        if(lable != None and lable != " " and "GRA Supply" in lable):
            GRA_text = contect_div[i].find("span",{"class":"outputText_DESCRIPTION-GRAY"})
            GRA_append = GRA_text.text.encode('utf-8')
            lable = lable.find("span")
        elif(lable != None and lable != " " and value != None):
            lable = lable.find("span")
            if(lable.contents[0].encode('utf-8') != ' '):
                tmp.append(lable.contents[0].encode('utf-8'))
                tmp.append(value.text.replace("'"," ").replace('"','').encode('utf-8'))
                overview_data[lable.contents[0].encode('utf-8').replace("\n","").replace("'","").replace('"','')] = str(value.text.encode('utf-8').replace("\xE2\x87\x92", "").replace("\n","").replace("'","").replace('"',''))
    
    overview_table.append(overview_data)
    
    ### ------------------------------ Who to contact  -------------------------
    tmp =  []
    tmp1 = []
    tmp2 = []
    checkpoint0 = 0    # checkpoint  
    
    for l in range (len(section_headings)):
        if "WHO TO CONTACT" in section_headings[l]:
            while i in range(4):             
                try:            
                    who_to_div = contect_div[i+1] 
                    who_to_title = who_to_div.find("div", {"class", "outputText_TITLE-BLACK"})
                    name_1 = who_to_div.findAll("div",{"class":["formOutputText_HIDDEN-LABEL", "outputText_TITLE-BLACK"]})
                    first_person = name_1[0].text.encode('utf-8').replace("\n","").replace("'","").replace('"','') 
                
                    phone1 = who_to_div.findAll("div", {"class": "formRow_HIDDEN-LABEL"})
                    
                    tmp1.append('Primary Contact: ' + first_person)
                    index = 0
                    try:
                        if "@" in phone1[index].text.encode('utf-8'):
                            tmp1.append('email: ' + phone1[index].text.encode('utf-8'))
                            index = index + 1
                            email_counter == email_counter + 1
                            print "email_counter = " + str(email_counter)
                            if email_counter > 10:
                                return None
                        else:
                            if email_counter == 0:
                                lookup(driver, "Selenium")
                                email_counter == email_counter + 1
                    except: 
                        index = index
                    try:
                        tmp1.append('Phone 1: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        index = index + 1 
                    except:
                        index = index
                    try:    
                        tmp1.append('Phone 2: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        index = index + 1 
                    except:
                        index = index
                    try:        
                        if "@" not in phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''):
                            tmp1.append('Address: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                            index = index +1
                    except:
                        tmp1.append('Address: ' )
                        index = index
                        
                    #print tmp1 
                    overview_table.append(tmp1)
                    checkpoint0 = 5 # checkpoint 
                    
                    try:
                        second_person = name_1[1].text.encode('utf-8') #Alan Teo Chun Siong
                        tmp2.append('Secondary Contact: ' + second_person)
                        try:
                            tmp2.append('email: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                            index = index + 1
                        except:
                            index = index
                        try:
                            tmp2.append('Phone 1: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                            index = index + 1
                        except:
                            index = index
                        try:
                            tmp2.append('Phone 2: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                            index = index +1
                        except:
                            index = index 
                        try:
                            tmp2.append('Address: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        except:
                            pass
                        overview_table.append(tmp2)
                    except:
                        #print "Secondary contact not found."   
                        overview_table.append("Secondary contact not found.")
                    #print "i = " + str(i)
                    break
                except:
                    i = i+1
                    
    if checkpoint0 != 5:
        overview_table.append("Primary contact not found")
        overview_table.append("Secondary contact not found")
                    
        # -----------------------Awarding Agency-------------------------------------------------------------------
    k = len(contect_div)
    t = 1
    p = len(section_headings)
    checkpoint1 = 0     
    for l in range (p):
        if "AWARDING AGENCY" in section_headings[l]:
            while t<k:
                try:   
                    a_agency = contect_div[t+1]
                    a_agency_name = a_agency.find("div",{"class","formOutputText_VALUE-DIV"}).text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
            
                    name_1 = a_agency.findAll("div",{"class":["formOutputText_HIDDEN-LABEL", "outputText_TITLE-BLACK"]})
                    first_person = name_1[0].text.encode('utf-8').replace("\n","").replace("'","").replace('"','') #Yap Chin Voon
                    
                    tmp3 =[]
                    tmp3.append('Awarding Agency: '+ a_agency_name )
                    phone1 = a_agency.findAll("div", {"class": "formRow_HIDDEN-LABEL"})        
                    tmp3.append('Contact Person Details: ' + first_person)
                    index = 0
                    try:
                        tmp3.append('email: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        index = index + 1
                    except:
                        index = index
                    try:
                        tmp3.append('Phone 1: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        index = index + 1
                    except:
                        index = index    
                    try:
                        tmp3.append('Phone 2: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        index = index + 1
                    except:
                        index = index
                    try:
                        tmp3.append('Address: ' + phone1[index].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                    except:
                        pass
                        
                    overview_table.append(tmp3)
                    checkpoint1 = 5
                    break                   
                except:
                    t = t+1
                    
    if checkpoint1 != 5:
        t = 1
        overview_table.append("Awarding agency not found.")                                    
        
    #-------------------------- SITE BRIEFING  ------------------------------------------------------
    k = len(contect_div)
    p = len(section_headings)
    checkpoint2 = 0      
    for l in range (p):
        while l < p:
            if "SITE BRIEFING" in section_headings[l]:
                if t < k:
                    try:
                        site_brief = inner_div.findAll("div",{"id":"contentForm:sitebriefingId"}) #formContainer_TABLE
                        #print site_brief
                        trs = site_brief[0].findAll("table", { "class" : "form2_ROW-TABLE" })
                        tmp_b = []
                        for tr in trs:
                            tmp = []
                            lable = tr.find("div", {"class": "form2_ROW-LABEL"})
                            if(lable != None):
                                lable = lable.find("span")
                                tmp.append(lable.contents[0].encode('utf-8').replace("\n","").replace("'","").replace('"',''))                     
                            value = tr.find("div", {"class": "formOutputText_VALUE-DIV"})                        
                            if(value != None):
                                tmp.append(value.text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                            tmp_b.extend(tmp)
                        
                        # Contact Person's Details
                        all_div = site_brief[0].findAll("table",{"class":"form2_ROW-TABLE"})
                        #print all_div
                        tmp_c =[]
                        try:
                            tmp_c.append("name")
                            tmp_c.append(all_div[4].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        except:
                            tmp_c.append("")
                        try:
                            tmp_c.append("email")
                            tmp_c.append(all_div[5].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))          
                        except:
                            tmp_c.append("")
                        try:
                            tmp_c.append("Phone1")
                            tmp_c.append(all_div[6].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        except:
                            tmp_c.append("")
                        try:
                            tmp_c.append("Phone2")
                            tmp_c.append(all_div[7].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        except:
                            tmp_c.append("")
                        try:
                            tmp_c.append("Address")
                            tmp_c.append(all_div[8].text.encode('utf-8').replace("\n","").replace("'","").replace('"',''))
                        except:
                            tmp_c.append("")
                            
                        #print "Printing: "
                        #print tmp_c
                        try:
                       	    test_string = ''.join(str(e).lower() for e in tmp_b)                                    
      		            if "venue" in test_string:
      		                checkpoint2 = 5
      		                t = k
      		                l = p 
       	                        tmp_b.extend(tmp_c)
       	                        #print tmp_b
       	                        overview_table.append(tmp_b)
       	                        break
                   	except:
                  	 t= t+1
                    except:
                        t= t+1                     
            l = l + 1
            
    if checkpoint2 != 5:   
        overview_table.append("Site briefing not found.") 
    
    #-------------------------- Items to Respond --------------------------------------------
    inner_div = inner_div.findAll("table", {"class", "formColumns_COLUMN-TABLE"})
    checkpoint3 = 0
    k = len(inner_div)
    l = len(contect_div)             
    i = 0
    for i in range (k):
        try:
            #print "trying..."
            item_to_div = inner_div[i]    
            item_to_div = item_to_div.findAll("table", {"class" : "formColumns_ROW-TABLE"})
            #item = item_to_div[0]
            items_to = []
            for item in item_to_div:
            #if item != None:
                tmp={}
        
                other = item.findAll("table", {"class" : "form2_ROW-TABLE"})
                title = other[2].find("div", {"class" : "formOutputText_HIDDEN-LABEL"})
        
                key = other[3].find("div", {"class": "form2_ROW-LABEL"})
                lable1 = key.find("span")
                value1 = other[3].find("div", {"class": "formOutputText_VALUE-DIV"})
        
                key = other[4].find("div", {"class": "form2_ROW-LABEL"})
                lable2 = key.find("span") 
                value2 = other[4].find("div", {"class": "formOutputText_VALUE-DIV"})
        
                key = other[5].find("div", {"class": "form2_ROW-LABEL"})
                lable3 = key.find("span")
                value3 = other[5].find("div", {"class": "formOutputText_VALUE-DIV"})
        
                tmp['Title'] = title.contents[0].encode('utf-8').replace("\n","").replace("'","").replace('"','')      
                tmp['Unit_of_Measurement']=value1.text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                tmp['Required_Quantity']=value2.text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                tmp['Remarks'] = value3.text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                
                # Data inside individual Item To Respond
                try:
                    tmp2 = {}
                    other = item.findAll("table",{"class":"formContainer_TABLE"})
                    title = other[0].findAll("div",{"class":"formSectionHeader2_TEXT"})    
                    title_text = title[0].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')                        
                    headers = other[0].findAll("span")
                    #print "Headers length : " + str(len(headers))
                    lable1 = headers[0].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                    lable2 = headers[1].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                    lable3 = headers[2].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                    lable4 = headers[3].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                    value1 = headers[4].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                    value2 = headers[5].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                    value3 = headers[6].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')
                    value4 = headers[7].text.encode('utf-8').replace("\n","").replace("'","").replace('"','')

                    tmp2['Info_Regarding'] = title_text      
                    tmp2[lable1] = value1
                    tmp2[lable2] = value2
                    tmp2[lable3] = value3
                    tmp2[lable4] = value4
                    
                    #print tmp2 
                    tmp.update(tmp2) 
                
                except:
                    pass  
                items_to.append(tmp)
                #print items_to
                
                if tmp != None:
                    checkpoint3 = 5
        except:
            pass
        if checkpoint3 == 5:
            i = k + 1
            break    
        i = i+1            
    
    if checkpoint3 == 5:        
        overview_table.append(items_to)
    else:
        overview_table.append("Items to respond not found")
        
    overview_table.append(hashlib.md5(url).hexdigest())
    overview_table.append(url)

    placeholders = '", "'.join(str(v) for v in overview_table)
    placeholders_keys = '", "'.join(str(v) for v in overview_table_key)       
    
#-----------------------------------------------------------------------------------------------------------------------
    conn = MySQLdb.connect(host= "localhost", user="root", passwd="Manuwas@6789", db="newgebiz")
    x = conn.cursor()

    sql = 'INSERT INTO `close_opportunity` (`Overview_Data`, `WHO_TO_CONTACT`, `WHO_TO_CONTACT1`, `Awarding_Agency`, `Site_Briefing`, `ITEMS_TO_RESPOND`, `url_md5`, `url`) VALUES ( "'+ placeholders +'" )'
    
    print sql    
    try:
       x.execute(sql)
       print "inserted"
       conn.commit()
       #r.sadd("close_opportunity_done", url)
       #r.rpush("close_opportunity_resp", url)
    except MySQLdb.Error, e:
       conn.rollback()
       print "MySQLdb Error"
       #try:
       #    print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
       #except IndexError:
       #    print "MySQL Error: %s" % str(e)
       #conn.rollback()
       #r.rpush("all_close_opportunity", url)           
    x.close()
    return None


def lookup2(driver, query):
    rand = random.randint(1, 10)
    time.sleep(rand)
    print url
    driver.implicitly_wait(1)
    driver.get(url)
    time.sleep(0.3)
    driver.implicitly_wait(1)

    try:
        tabs = driver.find_elements_by_class_name("formTabBar_TAB-BUTTON")
        #print tabs
        #inpt = driver.find_element_by_name('contentForm:j_idt89_TabAction_1')
        tabs[0].click()
        driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "outputText_TITLE-BLACK")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        #main_div = soup.find("div", {"id": "contentForm:j_idt89"})
        main_div = soup.find("div", {"class": "formTabBar_MAIN"})
        title = main_div.find("div", { "class" : "outputText_TITLE-BLACK" })
        print title.text
        resp['total'] = title.text
        accordion = main_div.find("div", {"id": "accordion1_formAccordionGroup_BODY-CONTENT"})
        respondents = accordion.findAll("td", { "class" : "formCollapsibleContainer_MAIN"})
        companies = []
        for respondent in respondents:
            respondent_di = {}
            res_title = respondent.find("div", { "class" : "formAccordion_TITLE-TEXT"})
            print res_title.text
            respondent_di['company'] = res_title.text
            res_bid = respondent.find("div", { "class" : "formAccordion_TITLE-BAR"})
            print res_bid.find("span").text
            respondent_di['bid'] = res_bid.find("span").text

            main_table = main_div.find("table", { "class" : "formContainer_TABLE"})
            items = main_table.findAll("table", { "class" : "formColumns_ROW-TABLE"})
            bids = []
            for item in items:
                bids_item = {}
                driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "outputText_TITLE-BLACK")))
                item_title = item.find("div", { "class" : "outputText_TITLE-BLACK"})
                print item_title.text
                bids_item['title'] = item_title.text
                driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "formOutputText_HIDDEN-LABEL")))
                item_title1 = item.find("div", { "class" : "formOutputText_HIDDEN-LABEL"})
                print item_title1.contents[0]
                bids_item['item1'] = item_title1.contents[0]
                print item_title1.contents[2]
                bids_item['item2'] = item_title1.contents[2]

                key = item.findAll("div", {"class": "form2_ROW-LABEL"})
                value = item.findAll("div", {"class": "formOutputText_VALUE-DIV"})
                lable = key[0].find("span")
                print lable.text
                bids_item[lable.text] = value[0].text
                print value[0].text

                lable = key[1].find("span")
                print lable.text
                print value[1].text
                bids_item[lable.text] = value[1].text


                bid_table = item.find("table", { "class" : "table_MAIN"})
                bid_values = bid_table.findAll("td", {"class" : "table_TABLE-CELL-TD"})
                print "S/No : " + bid_values[0].text
                bids_item["s_no"] = bid_values[0].text
                print "Unit of Measurement : " + bid_values[1].text
                bids_item["Unit_of_Measurement"] = bid_values[1].text
                print "Quantity : " + bid_values[2].text
                bids_item["Quantity"] = bid_values[2].text
                print "Unit Price : " + bid_values[3].text
                bids_item["Unit_Price"] = bid_values[3].text
                print "Total Price : " + bid_values[4].text
                bids_item["Total_Price"] = bid_values[4].text
                print "Remarks : " + bid_values[5].text
                bids_item["Remarks"] = bid_values[5].text
                bids.append(bids_item)

            respondent_di['bids_item'] = bids
            companies.append(respondent_di)
        resp['respondent'] = companies
        print resp
        
        conn = MySQLdb.connect(host= "localhost", user="root", passwd="Manuwas@6789", db="newgebiz")
        x = conn.cursor()
        url_md5 = hashlib.md5(url).hexdigest()
        sql = "UPDATE `close_opportunity` set respondents = '%s' where url_md5 = '%s'" % (MySQLdb.escape_string(json.dumps(resp)), url_md5)        
        print sql   
        try:
           x.execute(sql)
           print "inserted"
           conn.commit()
           #r.rpush("close_opportunity_rew", url)
        except MySQLdb.Error, e:
           conn.rollback()
           print "dsdsfgd"
           #try:
           #    print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
           #except IndexError:
           #    print "MySQL Error: %s" % str(e)
           #conn.rollback()
           #r.rpush("close_opportunity_resp", url)              
        x.close()
        return None
    except:
        return None
        print("something went wrong")

def lookup3(driver, query):
    rand = random.randint(1, 3)
    time.sleep(rand)
    print url
    driver.implicitly_wait(1)
    driver.get(url)
    time.sleep(0.3)
    driver.implicitly_wait(1)
    try:
        #inpt = driver.find_element_by_name('contentForm:j_idt89_TabAction_2')
        tabs = driver.find_elements_by_class_name("formTabBar_TAB-BUTTON")
        tabs[1].click()
        driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "outputText_TITLE-BLACK")))
        driver.implicitly_wait(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        main_div = soup.find("div", {"class": "formTabBar_MAIN"})
        divs = main_div.find_all("table", { "class" : "formColumns_ROW-TABLE"})
        awarding_div = divs[0]
        
        #title = awarding_div.find("div", { "class" : "outputText_TITLE-BLACK" })
        #print title.text
        tmp = []
        tmp.append(["Awarding Agency"])
        agency = {}
        all_trs = awarding_div.findAll("table", { "class" : "form2_ROW-TABLE"})
        tmp.append([str(all_trs[0].text).replace(",", ".")])
        print all_trs[0].text
        agency['title'] = all_trs[0].text
        item = all_trs[3]
        key = item.find("div", {"class": "form2_ROW-LABEL"})
        value = item.find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        tmp.append([lable.text, value.text])
        print lable.text
        print value.text
        agency[lable.text] = value.text

        item = all_trs[4]
        key = item.find("div", {"class": "form2_ROW-LABEL"})
        value = item.find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency[lable.text] = value.text
        tmp.append([lable.text, value.text])

        item = all_trs[5]
        key = item.find("div", {"class": "form2_ROW-LABEL"})
        value = item.find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency[lable.text] = value.text
        tmp.append([lable.text, value.text])

        item = all_trs[6]
        key = item.find("div", {"class": "form2_ROW-LABEL"})
        value = item.find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency[lable.text] = value.text
        tmp.append([lable.text, value.text])

        item = all_trs[7]
        key = item.find("div", {"class": "form2_ROW-LABEL"})
        value = item.find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency[lable.text] = value.text
        tmp.append([lable.text, value.text])

        rewd['rewarding'] = agency
        agency_to = {}
        awarded_div = divs[2].findAll("table", { "class" : "formColumns_COLUMN-TABLE"})
        tmp.append(["Awarded to"])
        all_trs = awarded_div[1].findAll("table", { "class" : "form2_ROW-TABLE"})
        print all_trs[0].text
        agency_to['title'] = all_trs[0].text
        tmp.append([all_trs[0].text])
        print all_trs[1].text
        agency_to['title'] = all_trs[1].text
        tmp.append([all_trs[1].text])
        
        
        divs1 = main_div.find_all("table", { "class" : "form2_ROW-TABLE"})
        
        com_info = divs1[9].find("div", { "class" : "outputText_TITLE-BLACK"})
        print "sunil"
        print com_info.text
        agency_to['company_name'] = com_info.text
        
        com_info = divs1[10].find("div", { "class" : "outputText_NAME-BLACK"})
        print "sunil"
        print com_info.text
        agency_to['address'] = com_info.text

        key = awarded_div[1].find("table", {"class": "formContainer_TABLE"}).findAll("table")
        item = key[1].findAll("table", {"class": "form2_ROW-TABLE"})

        key = item[0].find("div", {"class": "form2_ROW-LABEL"})
        value = item[0].find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency_to[lable.text] = value.text
        tmp.append([lable.text, value.text])

        key = item[1].find("div", {"class": "form2_ROW-LABEL"})
        value = item[1].find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency_to[lable.text] = value.text
        tmp.append([lable.text, value.text])

        key = item[2].find("div", {"class": "form2_ROW-LABEL"})
        value = item[2].find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency_to[lable.text] = value.text
        tmp.append([lable.text, value.text])

        key = item[3].find("div", {"class": "form2_ROW-LABEL"})
        value = item[3].find("div", {"class": "formOutputText_VALUE-DIV"})
        lable = key.find("span")
        print lable.text
        print value.text
        agency_to[lable.text] = value.text
        tmp.append([lable.text, value.text])
        overview_table.append(tmp)
        
        rewd['rewarded'] = agency_to
        
        conn = MySQLdb.connect(host= "localhost", user="root", passwd="Manuwas@6789", db="newgebiz")
        x = conn.cursor()
        url_md5 = hashlib.md5(url).hexdigest()
        sql = "UPDATE `close_opportunity` set rewards = '%s' where url_md5 = '%s'" % (MySQLdb.escape_string(json.dumps(rewd)), url_md5) 
               
        print sql   
        try:
           x.execute(sql)
           print "inserted"
           conn.commit()
           #r.rpush("close_opportunity_done", url)
        except MySQLdb.Error, e:
           conn.rollback()
        x.close()
        
        if (time.time() - code_start < 1700):
            pass
        else:
            try:
                driver.quit()
                driver.close()
            except:
                pass
            display.stop()
            sys.exit()
        return None
    except:
        print("Box or Button not found on web")
        #code stops in 1700 seconds
        if (time.time() - code_start < 1700):
            pass
        else:
            try:
                
                driver.quit()
                driver.close()
            except:
                pass
            display.stop()
            sys.exit() 
        
if __name__ == "__main__":
    driver = init_driver()
    conn2 = MySQLdb.connect(host= "localhost", user="root", passwd="Manuwas@6789", db="newgebiz")
    sql2 = "SELECT * FROM close_opportunity;"
    y = conn2.cursor()
    y.execute(sql2)
    number_rows = len(y.fetchall()) 
    conn2.commit() 
    print number_rows
    
    data_not_found = [] 
    total_count = 0 
    code_start = time.time()      
                
    for index in range(len(urlarray)):
        try:
            if index % 20 == 0 :
                driver.get("https://www.google.com/")
                driver.delete_all_cookies()
                driver.implicitly_wait(10)
                                
            if index % 30 == 0 :
                driver.get("https://mail.google.com/")
                driver.delete_all_cookies()
                driver.implicitly_wait(21)
                
            line = urlarray[index + 20720-291].replace("\n","") #line
            
                 
            total_count = total_count + 1  
            print "Index: " + str(total_count)
            check_var = 0
            start = time.time()

            while (time.time() - start < 40):
                check_value = 0
                if check_value == 0:
                    check_value = 1     
                    email_counter = 0

                    url = line.replace("\n","")
                    try:
                        lookup(driver, "Selenium") #Overview
                    except:
                        pass
                    try:    
                        resp = {}
                        overview_table = []
                        lookup2(driver, "Selenium") #Respondent
                    except:
                        pass
                    try:
                        overview_table = []
                        rewd = {}
                        lookup3(driver, "Selenium") #Reward
                        break
                    except:
                        pass        
    
        except Exception,e: 
            print str(e)
    
    time.sleep(1)
    driver.quit()
    display.stop()
    print "closed"

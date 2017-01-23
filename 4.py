from __future__ import print_function
import httplib2
from datetime import date
import os
from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools
import base64
import email
import json
import cjson
import MySQLdb
from bs4 import BeautifulSoup
import quopri
from urlparse import urlparse
import re
from tld import get_tld
import hashlib
from dateutil.parser import parse


connection = MySQLdb.connect(host= "", user="", passwd="", db="")
cursor = connection.cursor()

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)
        
    
def MessageDetails(id_table, msg_id, msg_str): 
  try:
    print ("message_id = " +  str(msg_id))
    msg = email.message_from_string(msg_str)  
    
    date_mail1 = str(parse(msg['Date']))
    date_mail2 = date_mail1.split("+")
    date_mail = date_mail2[0]
  
    # -----------------------  Newsletter --------------------------------------
    try:
        from_mail =  msg['From']       
        newsletter_split = from_mail.split("@")
        newsletter = newsletter_split[len(newsletter_split)-1].replace(">","")
        print ("newsletter = " + str(newsletter))
        newsletter_complete_split = from_mail.split("<")
        newsletter_complete = newsletter_complete_split[1].replace(">","")
        print ("newsletter_complete = " + str(newsletter_complete))
    except:
        pass
    # ----------------------- Message Content ----------------------------------
    
    global x
    x = 0
    complete_message = []
    links = []
    html_content = []
    #print ("Message Length = " + str(len(msg)))
    for part in msg.walk(): 
        if part.get_content_type() == 'text/html':    
            try:
                decoded_html = quopri.decodestring(part.get_payload())
                html_content.append(decoded_html)
                decoded_html = decoded_html.replace("'","").replace('"',"")
            except:
                pass
            try:    
                soup = BeautifulSoup(decoded_html,'html.parser')            
                complete_message.append(soup)
            
                anchors = soup.findAll('a')        
                for a in anchors:
                    links.append(str(a['href']))
                    #print (str(a['href']))
            except:
                pass
             

        elif part.get_content_type()  == 'text/plain':
            pass
    try:
        html_content = str(base64.b64encode(html_content[0]))
    except:
        html_content = ""    

    try:
        url_distinct = []
        url_times_dict = []
        tld_distinct = []
        tld_index_dict = []
        ser_no = 0
        ser_no_tld = 0
        total_links_mail = len(links)
        for urls in links:
            if urls not in url_distinct:
                url_distinct.append(urls)
                tmp = {}
                ser_no = ser_no + 1
                tmp['ser_no'] = ser_no
                tmp['url'] = urls
                tmp['count'] = links.count(urls)
                tmp['tld'] = get_tld(urls)
                url_times_dict.append(tmp)
                if str(get_tld(urls)) not in tld_distinct:
                    tld_distinct.append(get_tld(urls))
                    ser_no_tld = ser_no_tld + 1
                    tmp_tld = {}
                    tmp_tld['ser_no'] = ser_no_tld
                    tmp_tld['tld'] = get_tld(urls)
                    tld_index_dict.append(tmp_tld)

        for items in url_times_dict:
            urlx = items['url']
            countx = items['count']
            tldx = items['tld']
            positionx = items['ser_no']
            tld_index = ""
            
            for tlds in tld_index_dict:
                if tlds['tld'] == tldx:
                    tld_index = tlds['ser_no']
                    break
            
            url_short1 = urlx.split(tldx) 
            url_short = url_short1[len(url_short1) - 1]
            unique_hash = hashlib.md5(str(positionx) + str(urlx) + str(countx) + str(tldx)).hexdigest()
            sql_command = "INSERT INTO `message_body` (`all_messages_id`, `message_id`, `newsletter`,  `newsletter_complete`, `tld`, `tld_index`,  `website_url`, `website_index`, `url_count_times`, `date_mail`, `total_links_mail`, `url_short`, `html_content`, `unique_hash`) VALUES (" + "'" + str(id_table) + "'" + "," + "'" + str(msg_id) + "'" + "," + "'" + str(newsletter) + "'" + "," +  "'"+ str(newsletter_complete) +"'" + "," + "'" + str(tldx) + "'" + ","  + "'" + str(tld_index) + "'" + "," +  "'"+ str(urlx) +"'" + "," + "'" +  str(positionx) + "'" + "," +  "'"+ str(countx) +"'" + "," + "'" +  str(date_mail) + "'" + "," +  "'"+ str(total_links_mail) +"'" + "," +  "'"+ str(url_short) +"'" + "," +  "'"+ str(html_content) +"'" + "," + "'"+ str(unique_hash) +"'"  + ")"
            print (sql_command)
            cursor.execute(sql_command)
            connection.commit()
    except:
        print ("errors found here")
        pass
  
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)     



if __name__ == '__main__':
    all_message_dict = []
    cursor.execute ("SELECT `id`, `message_id`, `message_content` FROM `all_messages`;")
    data = cursor.fetchall()
    for row in data:
        tmp = {}
        tmp['id'] = int(row[0])
        tmp['message_id'] = row[1] 
        tmp['message_content'] = row[2];
        all_message_dict.append(tmp)     
     
    for each_dict in all_message_dict:
        id_table = each_dict['id']
        msg_id = each_dict['message_id']
        message_content = base64.b64decode(each_dict['message_content'])
        message_json = json.loads(message_content.encode('ASCII'))
        msg_str = base64.urlsafe_b64decode(message_json['raw'].encode('ASCII'))
        MessageDetails(id_table, msg_id, msg_str)

             

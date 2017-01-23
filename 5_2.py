# !/usr/bin/python

import requests
from bs4 import BeautifulSoup

with open('xya.txt') as f:
    urlarray = []
    for line in f:
        urlarray.append(line) 
        
print "Searching for links in " + str(len(urlarray)) + " urls...."

pagelinks_ws = []
for i in range(len(urlarray)): #in range (1):
    url = urlarray[i].replace("\n", "")
    print i
    print url
    r = requests.get(url)
    r.raise_for_status()
    print r.status_code
    soup = BeautifulSoup(r.content,'html.parser')
    main = soup.find_all("div", {"class": ["well" ,"result-box" ,"nomargin"]})
    for k in main:
        links = k.findAll("a", href=True)
        for item in links:            
            if "c" in item['href']:
               pagelinks_ws.append(l)
                                
print len(pagelinks_ws)

def get_distinct(pagelinks_ws): 
    distinct_list = []
    for each in pagelinks_ws:
        if each not in distinct_list:
            distinct_list.append(each)
    return distinct_list 

pagelinks_ws = get_distinct(pagelinks_ws)   
print "Total pagelinks not containing 'skin' found:"
print len(pagelinks_ws) 


f = open("xyasd", "w") # Write Text File
mylist = pagelinks_ws
f.write("\n".join(map(lambda x: str(x), pagelinks_ws)) + "\n")  
f.close()

    
    

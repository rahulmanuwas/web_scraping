import requests
from bs4 import BeautifulSoup

url = ""

r = requests.get(url)
r.raise_for_status()
soup = BeautifulSoup(r.content,'html.parser')

## ----------- Get all urls ----------------------------------
all_urls = []

item  = ["weapon", "case", "collection", "sticker", "tournament", "music", "item" , "family", "container"]
for url in soup.find_all("a"):
    k = url.get("href")
    if k != None and "https://xhsj.com/" in k and "steamcommunity" not in k:
        if "setcurrency" not in k:
            if k in item:
                if "xyz" not in k:
                    all_urls.append(k.encode('utf-8')) 

def get_distinct(all_urls):
    distinct_list = []
    for each in all_urls:
        if each not in distinct_list:
            distinct_list.append(each)
    return distinct_list 

all_urls = get_distinct(all_urls)  # Unique urls  
print "Total urls found by Beautiful Soup:"
print len(all_urls)  


f = open("changed.txt", "w")
mylist = all_urls
f.write("\n".join(map(lambda x: str(x), all_urls)) + "\n")  
f.close()


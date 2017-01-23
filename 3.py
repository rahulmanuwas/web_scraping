import requests
import MySQLdb


conn = MySQLdb.connect(host= " ", user="", passwd="", db="")

def getSchemeDetails():
    url = ""

    params = {'ID':28}
    r = requests.post(url, params=params)

    print r.status_code
    print r.content

getSchemeDetails()

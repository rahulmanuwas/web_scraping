import MySQLdb

db = MySQLdb.connect()        
cursor = db.cursor()

with open('value') as f:
    urlarray = []
    for line in f:
        urlarray.append(line)             
print "Value :" + urlarray[0]                                    
value = urlarray[0]
sql_command = "SELECT * FROM TABLEX;"        
cursor.execute(sql_command)
result = cursor.fetchall()

for row in result:
  print row
  
print "We have " + str(len(result)) + "  itemes that meet your needs."  

db.commit()

db.close()
                

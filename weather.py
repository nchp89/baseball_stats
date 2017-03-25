import urllib
import json
import sqlite3

key_ID = "bec14c364e8e0a3f"
serviceurl = "http://api.wunderground.com/api/"

#urllib2.urlopen('http://api.wunderground.com/api/bec14c364e8e0a3f/geolookup/conditions/q/IA/Cedar_Rapids.json')

conn = sqlite3.connect('weatherdb.sqlite')
cursor = conn.cursor()

#delete existing table of weather
cursor.execute('''
DROP TABLE IF EXISTS SixHour4cast''')
#create new table
cursor.execute('''
CREATE TABLE SixHour4cast(cityname TEXT, timetemp1 TEXT, timetemp2 TEXT, timetemp3 TEXT, timetemp4 TEXT, timetemp5 TEXT, timetemp6 TEXT)''')

while True:
    #get location of weather forecast desired
    location = raw_input("Format : ST/City_Name : ")
    if len(location) == 0:
        break
    if len(location) == 1:
        location = "MO/Saint_Louis"
      
    data = urllib.urlopen(serviceurl + key_ID + "/hourly/q/" + location + ".json").read()
    parsed_data = json.loads(data)
    #print json.dumps(parsed_data, indent = 4)
    
    try:
        if parsed_data["response"]["error"]:
            print "City not found"
            continue
    except:
        pass
    
    #make a list to hold info
    ttlist = [location]
    for i in range(0,6):
        time = parsed_data["hourly_forecast"][i]["FCTTIME"]["civil"] 
        condition = parsed_data["hourly_forecast"][i]["condition"]
        temp = parsed_data["hourly_forecast"][i]["feelslike"]["english"] + "*F"
        ttlist.append(time + " :: " + condition + " :: " + temp)
    
    cursor.execute('''
    INSERT INTO SixHour4cast VALUES (?, ?, ?, ?, ?, ?, ?)''', tuple(ttlist))
    
conn.commit()
cursor.close()
conn.close()
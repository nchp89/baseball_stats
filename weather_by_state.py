import urllib
import json
import time
import sqlite3

#key ID and service URL to communicate to wunderground.com API
key_ID = "bec14c364e8e0a3f"
serviceurl = "http://api.wunderground.com/api/"

#open connection and create cursor to DB
conn = sqlite3.connect('weatherdb.sqlite')
cursor = conn.cursor()

#delete existing table of weather
cursor.execute('''
DROP TABLE IF EXISTS WeatherByStates''')
#create new table
cursor.execute('''
CREATE TABLE WeatherByStates (state TEXT, 
                              cityname TEXT, 
                              forecast TEXT, 
                              temperature TEXT, 
                              rel_humid TEXT, 
                              wind_speed TEXT, 
                              wind_direction TEXT, 
                              feels_like TEXT)''')


#open state_capitols.txt
capitols = open("state_capitols.txt")
temperatures = {}

for location in capitols:
    #get json from wunderground and parse it
    data = urllib.urlopen(serviceurl + key_ID + "/conditions/q/" + location + ".json").read()
    parsed_data = json.loads(data)
    #sleep for 7 second to stay under 10 calls a minute to wunderground API
    time.sleep(7)
    try:
        co = parsed_data["current_observation"]
        temperatures[co["observation_location"]["state"]] = [location.split('/')[0],
                                                            location.split('/')[1],
                                                            co["weather"],
                                                            co["temperature_string"],
                                                            co["relative_humidity"], 
                                                            co["wind_mph"],
                                                            co["wind_dir"], 
                                                            co["feelslike_string"]]
        
        cursor.execute('''
        INSERT INTO WeatherByStates VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', tuple(temperatures[co["observation_location"]["state"]]))
    except:
        pass
 
conn.commit()
cursor.close()
conn.close()
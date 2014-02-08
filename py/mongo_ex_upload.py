# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 21:13:04 2014

@author: mohammad
"""

# You need to install pymongo, mysql-python and twitter

import twitter
import pymongo as pym
import MySQLdb
import json
import pprint

"""
# After you have added the employee example database you can query from 
# within python or through any other means

# establish a connection
sqlconnection = MySQLdb.connect(host='127.0.0.1', #this is usually your local
                                user = 'root' , 
                                passwd = 'password', 
                                db='')

sqlcursor = sqlconnection.cursor()

#execute a query
sqlcursor.execute("select dept_no , dept_name from departments")
dep_data = sqlcursor.fetchall()

for row in dep_data:
    print row[0],row[1]
 
sqlcursor.close()
sqlconnection.close()
"""

# Connect to twitter API
CONSUMER_KEY = 'zr7offwmXUnvGg1OS1yzQ'
CONSUMER_SECRET = 'S6qBCjLNkOyXJgXyuEDelBnuGvpD525w9imCCQkjI'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# Nothing to see by displaying twitter_api except that it's now a
# defined variable

print twitter_api

WORLD_WOE_ID = 1
US_WOE_ID = 23424977
AUS_WOE_ID = 23424748
SYD_AUS_WOE_ID = 1105779
MEL_AUS_WOE_ID = 1103816



# Get trending data from twitter

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
us_trends = twitter_api.trends.place(_id=US_WOE_ID)
aus_trends = twitter_api.trends.place(_id=AUS_WOE_ID)
syd_trends = twitter_api.trends.place(_id=SYD_AUS_WOE_ID)
mel_trends = twitter_api.trends.place(_id=MEL_AUS_WOE_ID)

# lets load this into our MongoDB in the twit database
#first establish connection to Server - DB - Collection

mongoconnection = pym.MongoClient(host = 'localhost')
mngodb = mongoconnection.twit
mngocoll = mngodb.trends

#now insert only 1 to test
mngocoll.insert(aus_trends)
mngocoll.find().count()
mngocoll.remove()


# lets insert all
mngocoll.find().count()
mngocoll.insert(world_trends) 
mngocoll.insert(us_trends) 
mngocoll.insert(aus_trends) 
mngocoll.insert(syd_trends) 
mngocoll.insert(mel_trends)
mngocoll.find().count()

print mngocoll.find().count()
#print mngocoll.find()[0]

pprint.pprint(mngocoll.find()[0])
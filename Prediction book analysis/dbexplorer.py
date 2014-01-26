# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 18:31:15 2014

@author: ben
"""
#!/usr/bin/python

# using the tutorial found here:
# http://mysql-python.sourceforge.net/MySQLdb.html

import MySQLdb

# Open database connection
db = MySQLdb.connect(user = 'root', 
                     passwd = 'password',
                     db = 'mysql', 
                     host = 'localhost')


db.query("select * from users ")
result = db.store_result()
print "result:",result.fetch_row()
"""
# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data
"""
# disconnect from server
db.close()
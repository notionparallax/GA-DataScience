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


db.query("""select * from  mysql.predictions p
	left outer join mysql.responses r
		on p.id = r.prediction_id 
left outer join mysql.judgements j
		on p.id = j.prediction_id """)
result = db.store_result()
print result.fetch_row(maxrows=1, how=2) 
#max=0 means all, how=0 means tuple, how=1-dict, how=2 dict with fully qualified names

# disconnect from server
db.close()
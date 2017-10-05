
import sqlite3
import csv
from pprint import pprint
sqlite_file = 'bucharest.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()
#number of nodes and ways
QUERY = "select COUNT(*) from nodes "
cur.execute(QUERY)
result = cur.fetchone()
print "Number of nodes:", result[0]


QUERY = "select COUNT(*) from ways "
cur.execute(QUERY)
result = cur.fetchone()
print "Number of ways:", result[0]


#number of unique users
QUERY = "select count(distinct uid) from (select uid from nodes union all select uid from ways)"
cur.execute(QUERY)
result = cur.fetchone()
print "Number of unique users:", result[0]

#top 3  contributing users
QUERY = "SELECT user, count(*) as USERS_COUNT \
         FROM (select user, uid from nodes UNION ALL select user, uid FROM ways) \
         GROUP BY user \
         ORDER BY USERS_COUNT DESC \
         LIMIT 3"
cur.execute(QUERY)
result = cur.fetchall()
print "----top 3  contributing users----"
c=1
for i in result:
    print c,"User name: %s, Posts counts: %s" % (i[0], i[1])
    c+=1

#number of users contributing once
QUERY = "SELECT count(*) FROM \
         (SELECT user, count(*) as USERS_COUNT \
         FROM (select user, uid from nodes UNION ALL select user, uid FROM ways) \
         GROUP BY user \
         HAVING USERS_COUNT=1)"
cur.execute(QUERY)
result = cur.fetchone()
print "----Users contributing once----"
print "Number of users contributing once:", result[0]


#number of mobile shops
QUERY = "SELECT value, count(*)\
         FROM nodes_tags WHERE  value in ('Telekom','Orange','Vodafone') \
         GROUP BY value"
cur.execute(QUERY)
result = cur.fetchall()
print "----Mobile shops----"
for i in result:
    print "Shop name: %s, counts: %s" % (i[0], i[1])


#operator with most shops
QUERY = "SELECT value, max(No_shops) FROM \
          (SELECT value, count(*) as No_shops\
           FROM nodes_tags WHERE value IN ('Telekom','Orange','Vodafone') \
           GROUP BY value)" 
cur.execute(QUERY)
result = cur.fetchall()
print "----Mobile operator with most shops----"
for i in result:
    print "Shop name: %s, max counts: %s" % (i[0], i[1])

#Shops position on map
QUERY = "SELECT value, lon, lat FROM (\
        (SELECT id, value  \
            FROM nodes_tags WHERE value IN ('Telekom','Orange','Vodafone')) t_shops \
          LEFT JOIN \
           (SELECT DISTINCT id, lon, lat\
             FROM nodes) t_pos \
          ON t_shops.id=t_pos.id)" 
cur.execute(QUERY)
result = cur.fetchall()
print "----Mobile shops position on map----"
for i in result:
    print "Shop name: %s, Lat: %s, Lon: %s" %(i[0], i[1], i[2])

#Min and Max date by shop when the shop was updated on the map 
QUERY = "SELECT value, MIN(SUBSTR(timestamp,1,10)), MAX(SUBSTR(timestamp,1,10))FROM (\
        (SELECT id, value  \
            FROM nodes_tags WHERE value IN ('Telekom','Orange','Vodafone')) t_shops \
          LEFT JOIN \
           (SELECT distinct id, timestamp\
             FROM nodes) t_date \
          ON t_shops.id=t_date.id) fin_table \
         GROUP BY fin_table.value  " 
cur.execute(QUERY)
result = cur.fetchall()

import sqlite3
import csv
from pprint import pprint
sqlite_file = 'bucharest.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()
#number of nodes and ways
QUERY = "select COUNT(*) from nodes "
cur.execute(QUERY)
result = cur.fetchone()
print "Number of nodes:", result[0]


QUERY = "select COUNT(*) from ways "
cur.execute(QUERY)
result = cur.fetchone()
print "Number of ways:", result[0]


#number of unique users
QUERY = "select count(distinct uid) from (select uid from nodes union all select uid from ways)"
cur.execute(QUERY)
result = cur.fetchone()
print "Number of unique users:", result[0]

#top 3  contributing users
QUERY = "SELECT user, count(*) as USERS_COUNT \
         FROM (select user, uid from nodes UNION ALL select user, uid FROM ways) \
         GROUP BY user \
         ORDER BY USERS_COUNT DESC \
         LIMIT 3"
cur.execute(QUERY)
result = cur.fetchall()
print "----top 3  contributing users----"
c=1
for i in result:
    print c,"User name: %s, Posts counts: %s" % (i[0], i[1])
    c+=1

#number of users contributing once
QUERY = "SELECT count(*) FROM \
         (SELECT user, count(*) as USERS_COUNT \
         FROM (select user, uid from nodes UNION ALL select user, uid FROM ways) \
         GROUP BY user \
         HAVING USERS_COUNT=1)"
cur.execute(QUERY)
result = cur.fetchone()
print "----Users contributing once----"
print "Number of users contributing once:", result[0]


#number of mobile shops
QUERY = "SELECT value, count(*)\
         FROM nodes_tags WHERE  value in ('Telekom','Orange','Vodafone') \
         GROUP BY value"
cur.execute(QUERY)
result = cur.fetchall()
print "----Mobile shops----"
for i in result:
    print "Shop name: %s, counts: %s" % (i[0], i[1])


#operator with most shops
QUERY = "SELECT value, max(No_shops) FROM \
          (SELECT value, count(*) as No_shops\
           FROM nodes_tags WHERE value IN ('Telekom','Orange','Vodafone') \
           GROUP BY value)" 
cur.execute(QUERY)
result = cur.fetchall()
print "----Mobile operator with most shops----"
for i in result:
    print "Shop name: %s, max counts: %s" % (i[0], i[1])

#Shops position on map
QUERY = "SELECT value, lon, lat FROM (\
        (SELECT id, value  \
            FROM nodes_tags WHERE value IN ('Telekom','Orange','Vodafone')) t_shops \
          LEFT JOIN \
           (SELECT DISTINCT id, lon, lat\
             FROM nodes) t_pos \
          ON t_shops.id=t_pos.id)" 
cur.execute(QUERY)
result = cur.fetchall()
print "----Mobile shops position on map----"
for i in result:
    print "Shop name: %s, Lat: %s, Lon: %s" %(i[0], i[1], i[2])

#Min and Max date by shop when the shop was included in openstreetmap 
QUERY = "SELECT value, MIN(SUBSTR(timestamp,1,10)), MAX(SUBSTR(timestamp,1,10))FROM (\
        (SELECT id, value  \
            FROM nodes_tags WHERE value IN ('Telekom','Orange','Vodafone')) t_shops \
          LEFT JOIN \
           (SELECT distinct id, timestamp\
             FROM nodes) t_date \
          ON t_shops.id=t_date.id)  \
         GROUP BY value  " 
cur.execute(QUERY)
result = cur.fetchall()
print "----First and last time each shop was updated----"
for i in result:
    print "Shop name: %s, Min date: %s, Max date: %s" %(i[0], i[1], i[2])

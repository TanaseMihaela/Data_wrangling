import sqlite3
import csv
from pprint import pprint
sqlite_file = 'bucharest.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS nodes''')
cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
cur.execute('''DROP TABLE IF EXISTS ways''')
cur.execute('''DROP TABLE IF EXISTS ways_nodes''')
cur.execute('''DROP TABLE IF EXISTS ways_tags''')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''CREATE TABLE nodes (id INTEGER,lat FLOAT,lon FLOAT,user TEXT,uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT)''')
cur.execute('''CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)''')
cur.execute('''CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT)''')
cur.execute('''CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)''')
cur.execute('''CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT,type TEXT)''')
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:

with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['lat'],i['lon'], i['user'].decode('utf-8'), i['uid'], i['version'].decode('utf-8'), i['changeset'], i['timestamp']) for i in dr]
cur.executemany("INSERT INTO nodes (id,lat,lon,user,uid,version,changeset,timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)


with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'].decode('utf-8'),i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dr]    
cur.executemany("INSERT INTO nodes_tags (id,key,value,type) VALUES (?, ?, ?, ?);", to_db)



with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['user'].decode('utf-8'),i['uid'],i['version'],i['changeset'].decode('utf-8'),i['timestamp']) for i in dr]
cur.executemany("INSERT INTO ways (id,user,uid,version,changeset,timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)



with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['node_id'],i['position']) for i in dr]
cur.executemany("INSERT INTO ways_nodes (id,node_id,position) VALUES (?, ?, ?);", to_db)


    
with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'].decode('utf-8'),i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dr]    
cur.executemany("INSERT INTO ways_tags (id,key,value,type) VALUES (?, ?, ?,?);", to_db)
conn.commit()


print "======================================="
print "nodes preview:"
cur.execute('SELECT * FROM nodes LIMIT 10')
rows = cur.fetchall()
pprint(rows)

print "======================================="
print "nodes_tags preview:"
cur.execute('SELECT * FROM nodes_tags LIMIT 10')
rows = cur.fetchall()
pprint(rows)

print "======================================="
print "ways preview:"
cur.execute('SELECT * FROM ways LIMIT 10')
rows = cur.fetchall()
pprint(rows)

print "======================================="
print "ways_nodes preview:"
cur.execute('SELECT * FROM ways_nodes LIMIT 10')
rows = cur.fetchall()
pprint(rows)

print "======================================="
print "ways_tags preview:"
cur.execute('SELECT * FROM ways_nodes LIMIT 10')
rows = cur.fetchall()
pprint(rows)


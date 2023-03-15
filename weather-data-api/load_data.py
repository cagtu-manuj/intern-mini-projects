import psycopg2
import os
from datetime import datetime

# read from files
# for filename in os.listdir(os.path.join(os.getcwd(), "wx_data")):
# with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode

conn = psycopg2.connect(host="localhost", dbname="postgres",
                        user="mk", password="acer1234", port=5432)

cur = conn.cursor()

with open(os.path.join(os.getcwd(), "wx_data", "USC00339312.txt"), "r") as file:
    table_name = str(file.name.split('/')[-1].split('.')[0])
    cur.execute("DROP TABLE IF EXISTS %s" % table_name)
    sql = cur.mogrify("""CREATE TABLE IF NOT EXISTS %s(
        date INT NOT NULL,
        tmin INT,
        tmax INT,
        rain INT
        );""" % (table_name))
    cur.execute(sql)
    for line in file.readlines():
        data = line.split("\t")
        data = [int(item.strip()) for item in data]
        data.insert(0, table_name.lstrip())
        data = tuple(data)
        sql = "Insert INTO %s (date, tmin, tmax, rain) VALUES (%s, %s , %s, %s);" % data
        cur.execute(sql)


conn.commit()
cur.close()
conn.close()

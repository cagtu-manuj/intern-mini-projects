import psycopg2
import os
import time

# read from files

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="mk", password="acer1234", port=5432
)

cur = conn.cursor()

start_time = time.time()
total_records = 0
total_tables = 0
for filename in os.listdir(os.path.join(os.getcwd(), "wx_data")):
    total_tables += 1
    with open(os.path.join(os.getcwd(), "wx_data", filename), "r") as file:
        table_name = str(file.name.split("/")[-1].split(".")[0])
        cur.execute("DROP TABLE IF EXISTS %s" % table_name)
        sql = cur.mogrify(
            """CREATE TABLE IF NOT EXISTS %s(
            date INT NOT NULL UNIQUE,
            tmin INT,
            tmax INT,
            rain INT
            );"""
            % (table_name)
        )
        cur.execute(sql)
        args = []
        for line in file.readlines():
            data = line.split("\t")
            data = [(item.strip()) for item in data]
            args.append(tuple(data))
            # data.insert(0, table_name.lstrip())
            # data = tuple(data)
            # # worry about sql injection later
            # sql = "Insert INTO %s (date, tmin, tmax, rain) VALUES (%s, %s , %s, %s);" % data
            # # execute many
            # cur.execute(sql)
            total_records += 1
        # args_str = ','.join(cur.mogrify(
        #     "(%s,%s,%s,%s)", x) for x in args)
        # cur.execute("INSERT INTO table VALUES " + args_str)

        args_str = ",".join(["(%s, %s, %s, %s)" % x for x in args])
        sql = "INSERT INTO %s VALUES " % table_name + args_str
        cur.execute(sql)

conn.commit()
cur.close()
conn.close()
end_time = time.time()
print(f"Total tables added: {total_tables}")
print(f"Total rows added: {total_records}")
print(f"Total time: {end_time - start_time}")

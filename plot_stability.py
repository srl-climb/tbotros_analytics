import csv
import sqlite3
import yaml
import os
import pathlib

from rosbags.highlevel import AnyReader

directory = "D:/T7 Back-Up/2023_10_18_Tethered Climbing Robot Test 6/Rosbag/20231018-141144"

# create reader instance and open for reading
with AnyReader([pathlib.Path(directory)]) as reader:
    print(reader.connections)

    for connection in reader.connections:
        print(connection.topic)
        for _, timestamp, rawdata in reader.messages([connection]):
            print(timestamp)
            print(reader.deserialize(rawdata, connection.msgtype))
            break



        print(timestamp)
        break

    """ connections = [x for x in reader.connections if x.topic == '/imu_raw/Imu']
    for connection, timestamp, rawdata in reader.messages(connections=connections):
         msg = reader.deserialize(rawdata, connection.msgtype)
         print(msg.header.frame_id) """




""" def search_by_extension(path: str, ext: str) -> str:

        for file in os.listdir(path):
             if file.endswith(ext):
                  return os.path.join(path, file)
             
        raise OSError('No file with extension {} found'.format(ext))


directory = "D:/T7 Back-Up/2023_10_18_Tethered Climbing Robot Test 6/Rosbag/20231018-141144"
directory = os.path.normpath(directory)
database = search_by_extension(directory, '.db3')
metadata = search_by_extension(directory, '.yaml')


with open(metadata, 'r') as stream:
    topics: list =  yaml.safe_load(stream)['rosbag2_bagfile_information']['topics_with_message_count']

try:
    con = sqlite3.connect(database)
except Exception as e:
     print(e)


cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

cursor.execute('SELECT * FROM topics;')
data = cursor.fetchall()
print(type(data))
print(data[0])
print(data[1])
print(data[2])
cursor.execute('Select * FROM messages WHERE topic_id=1;')
data = cursor.fetchall()
# id topic_id timestamp data
print(data[0][3].hex().decode('UTF-8'))
print(type([data[0]])) """

""" for topic in topics:
    folder = os.path.normpath(os.path.join(directory, topic['topic_metadata']['name'][1:]))
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
      
    cur.execute("SELECT * FROM {}".format(topic['topic_metadata']['name']))
    rows = cur.fetchall()
    print(rows)
      
    break

con.close() """

""" database = "D:/T7 Back-Up/2023_10_18_Tethered Climbing Robot Test 6/Rosbag/20231018-141144_0.db3"

con = sqlite3.connect(database)
cursor = con.cursor()
cursor.execute("select * from moz_places;")

with open("out.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) # write headers
    csv_writer.writerows(cursor)
    print('hi')

con.close() """
from __future__ import annotations
import csv
import matplotlib.pyplot as plt
import os
import tbotlib as tb

directory = '/media/climb/T7/2023_10_18_Tethered Climbing Robot Test 6/Rosbag/20231018-141144/csv'
description = '/media/climb/T7/2023_10_18_Tethered Climbing Robot Test 6/Description/tetherbot/tetherbot_light.pkl'

def read_columns(file: str) -> dict[str, list]:
    
    with open(file, 'r') as stream:
        reader = csv.DictReader(stream)
        columns: dict[str, list] = {name: [] for name in reader.fieldnames}
        for row in reader: 
            for (k,v) in row.items(): 
                columns[k].append(float(v))

    return columns

fig, ax = plt.subplots()
ax.set(xlabel='time (s)', ylabel='stablity', title='Platform stablity')
ax.grid()

data = read_columns(os.path.join(directory, 'platform0__platform_state_publisher__stability.csv'))
ax.plot(data['message_timestamp'], data['data'])
data = read_columns(os.path.join(directory, 'platform0__platform_state_publisher__stability2.csv'))
ax.plot(data['message_timestamp'], data['data'])
data = read_columns(os.path.join(directory, 'platform0__platform_controller__tether_tension.csv'))
ax.plot(data['rosbag_timestamp'], data['data_0'])
ax.plot(data['rosbag_timestamp'], data['data_1'])
ax.plot(data['rosbag_timestamp'], data['data_2'])
ax.plot(data['rosbag_timestamp'], data['data_3'])
ax.plot(data['rosbag_timestamp'], data['data_4'])
ax.plot(data['rosbag_timestamp'], data['data_5'])
ax.plot(data['rosbag_timestamp'], data['data_6'])
ax.plot(data['rosbag_timestamp'], data['data_7'])
ax.plot(data['rosbag_timestamp'], data['data_8'])
ax.plot(data['rosbag_timestamp'], data['data_9'])

fig, ax = plt.subplots()
ax.set(xlabel='x (m)', ylabel='y(m)', title='Platform and arm position')
ax.grid()
data = read_columns(os.path.join(directory, 'platform0__platform_state_publisher__pose.csv'))
ax.scatter(data['x'], data['y'], s=1)
data = read_columns(os.path.join(directory, 'platform0__platform_controller__target_pose.csv'))
ax.scatter(data['x'], data['y'], s=1)
data = read_columns(os.path.join(directory, 'rpparm0__arm_state_publisher__pose.csv'))
ax.scatter(data['x'], data['y'], s=1)
data = read_columns(os.path.join(directory, 'rpparm0__arm_controller__target_pose.csv'))
ax.scatter(data['x'], data['y'], s=1)

tbot: tb.TbTetherbot = tb.TbTetherbot.load(description)
data = {'x': [], 'y': []}
for hold in tbot.wall.holds:
    data['x'].append(hold.T_world.x)
    data['y'].append(hold.T_world.y)
ax.scatter(data['x'], data['y'], s=10)

plt.show()


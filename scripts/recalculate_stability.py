from __future__ import annotations
import csv
import tbotlib as tb
import numpy as np
import os

description = '/media/climb/T7/2023_10_18_Tethered Climbing Robot Test 6/Description/tetherbot/tetherbot_light.pkl'
directory = '/media/climb/T7/2023_10_18_Tethered Climbing Robot Test 6/Rosbag/20231018-141144/csv'

def read_columns(file: str) -> dict[str, list]:
    
    with open(file, 'r') as stream:
        reader = csv.DictReader(stream)
        columns: dict[str, list] = {name: [] for name in reader.fieldnames}
        for row in reader: 
            for (k,v) in row.items(): 
                columns[k].append(float(v))

    return columns


def find_nearest(array, value) -> int:

    array = np.asarray(array)
    i = (np.abs(array - value)).argmin()
    
    return i


def find_pose(pose: dict[str, list], timestamp: float):

    i = find_nearest(pose['message_timestamp'], timestamp)

    return tb.TransformMatrix([pose['x'][i], pose['y'][i], pose['z'][i], pose['qw'][i], pose['qx'][i], pose['qy'][i], pose['qz'][i]])


def find_tension(tension: dict[str, list], timestamp: float):

    i = find_nearest(tension['rosbag_timestamp'], timestamp)

    return np.array([tension['data_0'][i], tension['data_1'][i], tension['data_2'][i], tension['data_3'][i], tension['data_4'][i], 
                     tension['data_5'][i], tension['data_6'][i] ,tension['data_7'][i], tension['data_8'][i], tension['data_9'][i]], dtype=bool)


file = os.path.join(directory, 'platform0__platform_state_publisher__pose.csv')
platform0_pose = read_columns(file)
file = os.path.join(directory, 'platform0__platform_state_publisher__stability.csv')
platform0_stability = read_columns(file)
file = os.path.join(directory, 'platform0__platform_controller__tether_tension.csv')
platform0_tether_tension = read_columns(file)
file = os.path.join(directory, 'gripper0__gripper_state_publisher__pose.csv')
gripper0_pose = read_columns(file)
file = os.path.join(directory, 'gripper1__gripper_state_publisher__pose.csv')
gripper1_pose = read_columns(file)
file = os.path.join(directory, 'gripper2__gripper_state_publisher__pose.csv')
gripper2_pose = read_columns(file)
file = os.path.join(directory, 'gripper3__gripper_state_publisher__pose.csv')
gripper3_pose = read_columns(file)
file = os.path.join(directory, 'gripper4__gripper_state_publisher__pose.csv')
gripper4_pose = read_columns(file)


tbot: tb.TbTetherbot = tb.TbTetherbot.load(description)

for gripper in tbot.grippers:
    gripper.parent = tbot.wall

platform0_stability['message_timestamp'] = platform0_stability['message_timestamp']
platform0_stability['data'] = platform0_stability['data']

platform0_stability2 = []
for message_timestamp, rosbag_timestamp in zip(platform0_stability['message_timestamp'], platform0_stability['rosbag_timestamp']):
    
    tbot.grippers[0].T_world = find_pose(gripper0_pose, message_timestamp)
    tbot.grippers[1].T_world = find_pose(gripper1_pose, message_timestamp)
    tbot.grippers[2].T_world = find_pose(gripper2_pose, message_timestamp)
    tbot.grippers[3].T_world = find_pose(gripper3_pose, message_timestamp)
    tbot.grippers[4].T_world = find_pose(gripper4_pose, message_timestamp)
    tbot.platform.T_world = find_pose(platform0_pose, message_timestamp)
    tbot._tensioned = find_tension(platform0_tether_tension, message_timestamp)

    platform0_stability2.append({'message_timestamp': message_timestamp, 'data': tbot.stability()[0], 'rosbag_timestamp': message_timestamp})


file = os.path.join(directory, 'platform0__platform_state_publisher__stability2.csv')
with open(file, 'w+') as stream:
        reader = csv.DictWriter(stream, ['message_timestamp', 'data', 'rosbag_timestamp'])
        reader.writeheader()
        print(platform0_stability2)
        reader.writerows(platform0_stability2)
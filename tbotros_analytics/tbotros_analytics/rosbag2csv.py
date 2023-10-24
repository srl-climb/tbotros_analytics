import sys
import os
import pathlib
from custom_msgs.msg import *
from rosbags.highlevel import AnyReader
from rosbags.serde import deserialize_cdr
from rosbags.typesys import get_types_from_idl, register_types
from ament_index_python.packages import get_package_share_directory
from launch.logging import get_logger
from .writer import *


LOGGER = get_logger('rosbag2csv')


def register_msgs(pkg: str):
    # path where msgs of package pkg are installed
    path = os.path.join(get_package_share_directory(pkg), 'msg')
    
    for file in os.listdir(path):
             if file.endswith('.idl'):
                  # get message definition from idl file
                  msg_type = get_types_from_idl(pathlib.Path(os.path.join(path, file)).read_text())
                  # make message type available to rosbags serializers/deserializers
                  register_types(msg_type)


def rosbag2csv(directory: str):

    # extend rosbag type system with non standard messages
    register_msgs('custom_msgs')
    register_msgs('mocap_msgs')

    with AnyReader([pathlib.Path(directory)]) as reader:
        LOGGER.info('Opened database {}'.format(os.path.basename(directory)))

        path = pathlib.Path(directory, 'csv')
        path.mkdir(parents=True, exist_ok=True)

        for connection in reader.connections:
            file = os.path.normpath(os.path.join(path, connection.topic[1:].replace('/', '__')) + '.csv')

            with open(file, 'w+') as stream:
                LOGGER.info('Writing {}'.format(os.path.basename(file)))
                
                if connection.msgtype == 'custom_msgs/msg/Float64Stamped':
                    writer = Float64StampedMsgWriter(stream)
                elif connection.msgtype == 'custom_msgs/msg/Int16Stamped':
                    writer = Int16StampedMsgWriter(stream)
                elif connection.msgtype == 'geometry_msgs/msg/PoseStamped':
                    writer = PoseStampedMsgWriter(stream)
                elif connection.msgtype == 'std_msgs/msg/String':
                    writer = StringMsgWriter(stream)
                elif connection.msgtype == 'std_msgs/msg/Int8':
                    writer = Int8MsgWriter(stream)
                elif connection.msgtype == 'std_msgs/msg/Bool':
                    writer = BoolMsgWriter(stream)
                elif connection.msgtype == 'custom_msgs/msg/Float64Array':
                    writer = Float64ArrayMsgWriter(stream, 10)
                elif connection.msgtype == 'custom_msgs/msg/BoolArray':
                    writer = BoolArrayMsgWriter(stream, 10)
                elif connection.msgtype == 'mocap_msgs/msg/RigidBodies':
                    writer = RigidBodiesMsgWriter(stream, 2)
                elif connection.msgtype == 'mocap_msgs/msg/Markers':
                    writer = MarkersMsgWriter(stream, 25)
                else:
                    raise NotImplementedError(connection.msgtype) 
                
                for _, timestamp, rawdata in reader.messages([connection]):      
                    data = deserialize_cdr(rawdata, connection.msgtype)
                    writer.writemsg(timestamp, data)

        LOGGER.info('Closed database {}'.format(os.path.basename(directory)))


def main():

    if len(sys.argv) == 2:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()

    try:
        rosbag2csv(directory)
    except Exception as exc:
        LOGGER.error(str(exc))


if __name__ == '__main__':

    main()

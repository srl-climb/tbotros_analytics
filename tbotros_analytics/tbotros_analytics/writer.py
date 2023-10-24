import csv
from custom_msgs.msg import Float64Stamped, Int16Stamped, Float64Array, BoolArray
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String, Bool, Int8
from builtin_interfaces.msg import Time
from mocap_msgs.msg import RigidBodies, Markers
from tbotlib import TransformMatrix


def stamp2seconds(stamp: Time):

    return stamp.sec + stamp.nanosec * 10**(-9)


class MsgWriter(csv.DictWriter):
     
    def __init__(self, file: str, msgdict: dict = None):

        if msgdict is None:
            msgdict = {}
        
        if type(msgdict) is list:
            msgdict = dict(zip(msgdict, [None]*len(msgdict)))

        self.msgdict = msgdict
        self.msgdict['rosbag_timestamp'] = None

        super().__init__(file, self.msgdict.keys())

        self.writeheader()

    def writemsg(self, timestamp: int):

        self.msgdict['rosbag_timestamp'] = timestamp * 10**(-9) # nanosec to sec

        return self.writerow(self.msgdict)


class Float64StampedMsgWriter(MsgWriter):

    def __init__(self, file: str):

        super().__init__(file, ['message_timestamp', 'data'])

    def writemsg(self, timestamp: int, msg: Float64Stamped):

        self.msgdict['message_timestamp'] = stamp2seconds(msg.stamp)
        self.msgdict['data']  = msg.data

        return super().writemsg(timestamp)


class Int16StampedMsgWriter(MsgWriter):

    def __init__(self, file: str):

        super().__init__(file, ['message_timestamp', 'data'])

    def writemsg(self, timestamp: int, msg: Int16Stamped):

        self.msgdict['message_timestamp'] = stamp2seconds(msg.stamp)
        self.msgdict['data']  = msg.data

        return super().writemsg(timestamp)


class StringMsgWriter(MsgWriter):

    def __init__(self, file: str):

        super().__init__(file, ['data'])

    def writemsg(self, timestamp: int, msg: String):

        self.msgdict['data']  = msg.data

        return super().writemsg(timestamp)


class BoolMsgWriter(MsgWriter):

    def __init__(self, file: str):

        super().__init__(file, ['data'])

    def writemsg(self, timestamp: int, msg: Bool):

        self.msgdict['data']  = msg.data

        return super().writemsg(timestamp)
    

class Int8MsgWriter(MsgWriter):

    def __init__(self, file: str):

        super().__init__(file, ['data'])

    def writemsg(self, timestamp: int, msg: Int8):

        self.msgdict['data']  = msg.data

        return super().writemsg(timestamp)


class PoseStampedMsgWriter(MsgWriter):

    def __init__(self, file: str):

        super().__init__(file, ['message_timestamp', 'x', 'y', 'z', 'qw', 'qx', 'qy', 'qz', 'theta_x', 'theta_y', 'theta_z'])

    def writemsg(self, timestamp: int, msg: PoseStamped):

        theta = TransformMatrix([msg.pose.position.x, 
                                 msg.pose.position.y, 
                                 msg.pose.position.z, 
                                 msg.pose.orientation.w, 
                                 msg.pose.orientation.x, 
                                 msg.pose.orientation.y, 
                                 msg.pose.orientation.z]).decompose()[3:]
        
        self.msgdict['message_timestamp']   = stamp2seconds(msg.header.stamp)
        self.msgdict['x']       = msg.pose.position.x
        self.msgdict['y']       = msg.pose.position.y
        self.msgdict['z']       = msg.pose.position.z
        self.msgdict['qw']      = msg.pose.orientation.w
        self.msgdict['qx']      = msg.pose.orientation.x
        self.msgdict['qy']      = msg.pose.orientation.y
        self.msgdict['qz']      = msg.pose.orientation.z
        self.msgdict['theta_x'] = theta[0]
        self.msgdict['theta_y'] = theta[1]
        self.msgdict['theta_z'] = theta[2]

        return super().writemsg(timestamp)


class Float64ArrayMsgWriter(MsgWriter):

    def __init__(self, file: str, n: int):

        self.datakeys = ['data_{}'.format(i) for i in range(n)]
        
        super().__init__(file, self.datakeys)

    def writemsg(self, timestamp: int, msg: Float64Array):

        for datakey, dataval in zip(self.datakeys, msg.data):
            self.msgdict[datakey] = dataval

        return super().writemsg(timestamp)
    

class BoolArrayMsgWriter(MsgWriter):

    def __init__(self, file: str, n: int):

        self.datakeys = ['data_{}'.format(i) for i in range(n)]
        
        super().__init__(file, self.datakeys)

    def writemsg(self, timestamp: int, msg: BoolArray):

        for datakey, dataval in zip(self.datakeys, msg.data):
            self.msgdict[datakey] = int(dataval)

        return super().writemsg(timestamp)


class RigidBodiesMsgWriter(MsgWriter):

    def __init__(self, file: str, n: int):

        self.bodykeys = []
        for i in range(n):
            self.bodykeys.append(['body_{}_{}'.format(i, k) for k in ['x', 'y', 'z', 'qw', 'qx', 'qy', 'qz', 'theta_x', 'theta_y', 'theta_z']])

        super().__init__(file, ['message_timestamp'] + sum(self.bodykeys, []))

    def writemsg(self, timestamp: int, msg: RigidBodies):

        self.msgdict['message_timestamp'] = stamp2seconds(msg.header.stamp)

        for bodykey, body in zip(self.bodykeys, msg.rigidbodies):
            theta = TransformMatrix([body.pose.position.x, 
                                     body.pose.position.y, 
                                     body.pose.position.z, 
                                     body.pose.orientation.w, 
                                     body.pose.orientation.x, 
                                     body.pose.orientation.y, 
                                     body.pose.orientation.z]).decompose()[3:]

            self.msgdict[bodykey[0]] = body.pose.position.x
            self.msgdict[bodykey[1]] = body.pose.position.y
            self.msgdict[bodykey[2]] = body.pose.position.z
            self.msgdict[bodykey[3]] = body.pose.orientation.w
            self.msgdict[bodykey[4]] = body.pose.orientation.x
            self.msgdict[bodykey[5]] = body.pose.orientation.y
            self.msgdict[bodykey[6]] = body.pose.orientation.z
            self.msgdict[bodykey[7]] = theta[0]
            self.msgdict[bodykey[8]] = theta[1]
            self.msgdict[bodykey[9]] = theta[2]

        return super().writemsg(timestamp)


class MarkersMsgWriter(MsgWriter):

    def __init__(self, file: str, n: int):

        self.markerkeys = []
        self.n = n
        for i in range(n):
            self.markerkeys.append(['marker_{}_{}'.format(i, k) for k in ['x', 'y', 'z']])

        super().__init__(file, ['message_timestamp'] + sum(self.markerkeys, []))

    def writemsg(self, timestamp: int, msg: Markers):

        self.msgdict['message_timestamp'] = stamp2seconds(msg.header.stamp)

        for marker in msg.markers:
            if marker.marker_index < self.n:
                markerkey = self.markerkeys[marker.marker_index]
                self.msgdict[markerkey[0]] = marker.translation.x
                self.msgdict[markerkey[1]] = marker.translation.y
                self.msgdict[markerkey[2]] = marker.translation.z

        return super().writemsg(timestamp)
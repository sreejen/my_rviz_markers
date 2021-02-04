#!/usr/bin/env python

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import numpy as np


class MarkerBasics(object):

    def __init__(self):
        self.marker_objectlisher = rospy.Publisher('/marker_basic', Marker, queue_size=1)
        self.rate = rospy.Rate(1)
        self.init_marker(index=0,z_val=0)
    
    def init_marker(self,index=0, z_val=0):
        self.marker_object = Marker()
        self.marker_object.header.frame_id = "/map"
        self.marker_object.header.stamp    = rospy.get_rostime()
        self.marker_object.ns = "haro"
        self.marker_object.id = index
        self.marker_object.type = Marker.LINE_STRIP
        self.marker_object.action = Marker.ADD
        
        self.marker_object.pose.position.x = 0
        self.marker_object.pose.position.y = 0
        self.marker_object.pose.position.z = 0
        count = 0
        self.marker_object.points = []
        for i in range(2):
            my_point = Point()
            my_point.x = count*2
            my_point.y = count*1/4
            my_point.z = count*2/3
            count = 100 + count
            self.marker_object.points.append(my_point)
        
        self.marker_object.pose.orientation.x = 0
        self.marker_object.pose.orientation.y = 0
        self.marker_object.pose.orientation.z = 0.0
        self.marker_object.pose.orientation.w = 1.0
        self.marker_object.scale.x = 0.5
        #self.marker_object.scale.y = 1.0
        #self.marker_object.scale.z = 1.0
    
        self.marker_object.color.r = 0.0
        self.marker_object.color.g = 0.0
        self.marker_object.color.b = 1.0
        # This has to be, otherwise it will be transparent
        self.marker_object.color.a = 1.0
            
        # If we want it for ever, 0, otherwise seconds before desapearing
        self.marker_object.lifetime = rospy.Duration(0)
    
    def start(self):
        while not rospy.is_shutdown():
            self.marker_objectlisher.publish(self.marker_object)
            self.rate.sleep()
   

if __name__ == '__main__':
    rospy.init_node('marker_basic_node', anonymous=True)
    markerbasics_object = MarkerBasics()
    try:
        markerbasics_object.start()
    except rospy.ROSInterruptException:
        pass
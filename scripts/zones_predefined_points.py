#! /usr/bin/env python

import rospy
from jsk_recognition_msgs.msg import PolygonArray
from geometry_msgs.msg import Polygon, PolygonStamped, Point32, PointStamped
from std_msgs.msg import Header
import numpy as np


class Zone_Overlay():

    def __init__(self):
        self.point_received = False
        self.c_p = PointStamped()
        #self.subs = rospy.Subscriber("/clicked_point", PointStamped, self.callback)
        
    def callback(self,point):
        self.c_p = point
        global p_point_x
        global p_point_y
        global p_list

        if not ((self.c_p.point.x == p_point_x) and (self.c_p.point.y == p_point_y)):
            p_point_x = self.c_p.point.x
            p_point_y = self.c_p.point.y
            #temp = Point32(x = p_point_x, y = p_point_y)
            #p_list.append(temp)
            p_list.append([p_point_x,p_point_y])
            #print(p_list)
            self.point_received = True

    def show_values(self):
            rospy.loginfo("The x coordinate of point "+ str(self.c_p.point.x))
            rospy.loginfo("The y coordinate of point "+ str(self.c_p.point.y))
            rospy.loginfo("The z coordinate of point "+ str(self.c_p.point.z))

    def DynamicPolygon(self,header,p_list):
        """
        Dynamicly changing poligon
        """
        
        p = PolygonStamped()
        p.header = header
        
        # Minimum 3, otherwise the normals can't be calculated and gives error.
        
        for i in p_list:
            rospy.loginfo(i[0])
            rospy.loginfo(i[1])
            point_object = Point32(x= i[0], y= i[1])
            p.polygon.points.append(point_object)
        #rospy.loginfo(p)  
        return p

    def dynamic_custom_polygon_demo(self,zones_list):
        
        #rospy.init_node("polygon_array_dynamic")
        # /polygon_array_dynamic/output
        pub = rospy.Publisher("/polygon_array_dynamic/output", PolygonArray, queue_size=1)
        r = rospy.Rate(5)
        count = 0
        msg = PolygonArray()
        header = Header()
        header.frame_id = "world"
        header.stamp = rospy.Time.now()
        msg.header = header
        msg.polygons = []
        msg.labels = []
        msg.likelihood = []
        for i in zones_list:  
            #print(i) 
            msg.polygons.append(self.DynamicPolygon(header,i))
            msg.labels.append(count)
            msg.likelihood.append(np.random.ranf())
            count += 1
        
        rospy.loginfo("Publishing box")
        pub.publish(msg)
        r.sleep()    

    def collect_points(self):
        
        while not self.point_received:    
            self.subs = rospy.Subscriber("/clicked_point", PointStamped, self.callback)
            #self.show_values()
        self.point_received = False

def zones():
    global p_point_x
    global p_point_y
    global zones_list
    global p_list
    global count_pub 
    rospy.init_node('draw_zone_node', anonymous=True)
    zone_overlay_object = Zone_Overlay()
    # rospy.loginfo("Enter how many zones you want to mark")
    # num_zones = int(raw_input())
    # rospy.loginfo("Enter how many points you want to mark")
    # num_point = int(raw_input())
    rospy.on_shutdown(shutdownhook)
    rospy.loginfo("Program starting")
    while not ctrl_c:
    #while not poly_pub:
        p_point_x = 0.0
        p_point_y = 0.0
        i_p = 0
        while i_p != 4:
            rospy.loginfo("Collecting points")
            zone_overlay_object.collect_points()   
            i_p += 1
        #zone_overlay_object.show_values()
        zones_list.append(p_list)
        p_list = []
        rospy.loginfo("Creating bounding box")
        zone_overlay_object.dynamic_custom_polygon_demo(zones_list)


def shutdownhook():
        # works better than the rospy.is_shut_down()
        global ctrl_c
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
if __name__ == "__main__":
    p_point_x = 0.0
    p_point_y = 0.0
    count_pub = 0
    p_list = []
    zones_list = []
    ctrl_c = False
    poly_pub = False
    point_sub = False
    try :
        zones()
    except rospy.ROSInterruptException:
        pass
    
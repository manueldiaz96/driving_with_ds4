#!/usr/bin/env python3
# coding=utf-8

import roslib
import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import sys
import time

twist_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

def create_Twist(joy_msg):

	ls_h, ls_v, rs_h, l2_slide, r2_slide, rs_v, _, _, _, _, _, _, _, _ = joy_msg.axes 
	
	tw_msg = Twist()

	if ls_h != 0:
		tw_msg.angular.z= ls_h

	if ls_v != 0:
		tw_msg.linear.x= ls_v*0.5*(-(0.5*r2_slide)+1.5)

	if l2_slide != 1:
		tw_msg.linear.x = 0.0
	
	twist_pub.publish(tw_msg)


def main(args):
	rospy.init_node('ds4driver', anonymous=True)

	discrete_mode = False

	if discrete_mode:
		joy_sub = rospy.Subscriber("/j0/joy", Joy, create_Twist)
	else:
		joy_sub = rospy.Subscriber("/j1/joy", Joy, create_Twist)

	rospy.loginfo("ds4driver on \tDiscrete mode: {}".format(discrete_mode))
	try:
		rospy.spin()
	except KeyboardInterrupt:
		rospy.loginfo("Shutting down")


if __name__ == '__main__':
	main(sys.argv)
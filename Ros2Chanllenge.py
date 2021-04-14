#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import sys
import math
#/turtle1/Pose topic callback
def pose_callback(pose):
		rospy.loginfo("Robot X = %f : Y=%f :theta=%f\n",pose.x,pose.y,pose.theta)
def move_turtle(lin_vel,ang_vel):
                """"This is the main function which is used to control the turtle;
                    The main logic is to make a feedback control loop which will run till the time angle covered is 2.06 times pi (it has to be 2.06 insted of 2 because there is some rounding off error)
                    lemma-->d(theta)/d(t)=d(w)"""
		rospy.init_node('move_turtle', anonymous=True)#Initializing rospy
		pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)#publisher
		rospy.Subscriber('/turtle1/pose',Pose, pose_callback)#setting up subscriber
		rate = rospy.Rate(3) # 3Hz
		vel = Twist()#making a Twist object
		round1=1#round variable will tell us how many times the loop executed
		current_angle=0.000000#this is the spawning angle of the turtle
		T=rospy.Time.now().to_sec()#This is the initial time at which the program started executing

		while not rospy.is_shutdown():#This is the main control loop,which takes the feedback and than generates output accordingly
			vel.linear.x = lin_vel
			vel.linear.y = 0
			vel.linear.z = 0
			vel.angular.x = 0
			vel.angular.y = 0
			vel.angular.z = ang_vel
			rospy.loginfo("Linear Vel = %f: Angular Vel = %f",lin_vel,ang_vel)		  
			pub.publish(vel)
			rate.sleep()
			rospy.loginfo("round1 = %d",round1)
			t= rospy.Time.now().to_sec()
			current_angle = ang_vel*(t-T)
			if current_angle>=2.06*math.pi:
				vel.linear.x = 0
				vel.angular.z = 0.7
				pub.publish(vel)
				rate.sleep()
				break
         		round1+=1
if __name__ == '__main__':
	try:
		move_turtle(2.0,1.0)
	except rospy.ROSInterruptException:
		pass

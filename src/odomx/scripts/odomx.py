#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import tf
from tf.transformations import euler_from_quaternion

class CmdVelToOdomx:
    def __init__(self):
        rospy.init_node('cmd_vel_to_odomx', anonymous=True)
        
        # Initialize last command velocity time
        self.last_cmd_vel_time = rospy.Time.now()
        
        # Subscriber to cmd_vel
        self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)
        
        # Publisher to /odomx
        self.odomx_pub = rospy.Publisher('/odomx', Odometry, queue_size=10)
        
        # Transform broadcaster
        self.odom_broadcaster = tf.TransformBroadcaster()
        
        # Variables for position and orientation
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        # Spin to keep the script from exiting
        rospy.spin()

    def cmd_vel_callback(self, data):
        # This function is called when a cmd_vel message is received
        # For demonstration, we'll just republish this as an Odometry message with integrated position
        
        # Get the time difference between the current and previous cmd_vel messages
        dt = rospy.Time.now().to_sec() - self.last_cmd_vel_time.to_sec()
        
        # Integrate velocity to find position
        self.x += data.linear.x * dt * math.cos(self.theta)
        self.y += data.linear.x * dt * math.sin(self.theta)
        self.theta += data.angular.z * dt
        
        # Create an Odometry message
        odomx_msg = Odometry()
        # Set the frame IDs
        odomx_msg.header.frame_id = "map"  # This should be the parent frame ID
        odomx_msg.child_frame_id = "base_link"  # This should be the child frame ID

        odomx_msg.pose.pose.position.x = self.x
        odomx_msg.pose.pose.position.y = self.y
        odomx_msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        odomx_msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)
        
        # Publish the Odometry message
        self.odomx_pub.publish(odomx_msg)
        
        # Publish the transform
        self.odom_broadcaster.sendTransform(
            (self.x, self.y, 0),
            (0, 0, odomx_msg.pose.pose.orientation.z, odomx_msg.pose.pose.orientation.w),
            rospy.Time.now(),
            "base_link2",
            "odom"
        )
        
        # Store the current time for the next iteration
        self.last_cmd_vel_time = rospy.Time.now()
        
        # Access the data parameter
        print(odomx_msg)

if __name__ == '__main__':
    try:
        CmdVelToOdomx()
    except rospy.ROSInterruptException:
        pass
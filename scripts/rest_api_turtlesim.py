#! /usr/bin/env python

import os
import rospy
import threading
import time

from flask import Flask, request, jsonify
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

x = 0
y = 0
theta = 0

def ros_callback(msg):
    global x, y, theta
    x = msg.x
    y = msg.y
    theta = msg.theta 

threading.Thread(target=lambda: rospy.init_node('example_node', disable_signals=True)).start()
rospy.Subscriber('/turtle1/pose', Pose, ros_callback)
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

app = Flask(__name__)

@app.route('/pose', methods = ['GET'])
def getpose():
    return jsonify({'success': True, 'x' : str(x), 'y': str(y), 'theta': str(theta)}), 200

@app.route('/vel', methods = ['POST'])
def setpose():
    rq = request.get_json()
    msg = Twist()
    msg.linear.x = float(rq.get('linear', '0'))
    msg.angular.z = float(rq.get('angular', '0'))
    pub.publish(msg)
    time.sleep(1)
    return jsonify({'success': True, 'linear speed' :  str(msg.linear.x), 'angular speed' : str(msg.angular.z), 'x' : str(x), 'y': str(y), 'theta': str(theta)}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)

#!/usr/bin/env python

"""Extract images from a rosbag.
"""

import os
import argparse
import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def rostime2floatSecs(rostime):
    return rostime.secs + (rostime.nsecs / 1000000000.0)

def main():    
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("--bag_file", help="Input ROS bag.", default="2022-11-01-17-43-56.bag")
    parser.add_argument("--output_dir", help="Output directory.", default="imgs/")

    args = parser.parse_args()
    bag_file = args.bag_file #"_2019-03-27-22-30-28.bag" 
    output_dir = args.output_dir #"extractedImages/"
    # compressed = args.compressed #true false
    
    image_topic = "/teli_camera/image_raw/compressed"
    
    jpg_quality = 100
    compr = cv2.IMWRITE_JPEG_QUALITY
    quality = jpg_quality  # jpg quality is in [0,100] range, png [0,9]
    params = [compr, quality]
    
    bag = rosbag.Bag(bag_file, "r")
    bridge = CvBridge()

    print("Save images...")
    count = 0
    denom = 10
    for topic, msg, t in bag.read_messages(topics=[image_topic]):
        if count % denom == 0:
            cv_img = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
            if cv_img is None:
                print("nnonon")
                continue
            print(topic, t, cv_img)
            picSaveName = "{}_{}.jpg".format(msg.header.stamp.secs, msg.header.stamp.nsecs)
            print(picSaveName)
            picPath = os.path.join(output_dir, picSaveName)
            cv2.imwrite(picPath, cv_img, params)        
        count += 1
    bag.close()
    
    return

if __name__ == '__main__':
    main()
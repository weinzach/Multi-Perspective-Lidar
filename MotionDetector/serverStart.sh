#!/bin/bash

#Change into directory
cd ~/Multi-Perspective-Lidar/MotionDetector/
cd Server

sleep 5

#Start Node Loop
forever start serverSign.js

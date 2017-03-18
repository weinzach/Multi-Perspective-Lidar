#!/bin/bash

#Change into directory
cd ~/Multi-Perspective-Lidar/MotionDetector/

#Start Node Loop
forever start clientEmitter.js

#Start Python Loop
until python clientDetector.py; do
    echo "Server 'myserver' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done

#Stop Loop After Close
forever stop clienEmitter.js

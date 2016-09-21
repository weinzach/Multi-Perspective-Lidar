import numpy as np 
import pointrotation as pr

# Constant values
ANGLE_INDEX = 2
RADIUS_INDEX = 3
NEWSCAN_INDEX = 0
STEP_INDEX = 4
X_OFFSET = 45
Z_OFFSET = 25
#This function parses
def read_scans(file):
	with open(file, 'r') as f:
		raw_data = []
		scans = []
		for line in f:
			raw_data.append(line.rstrip().split('\t'))

		scan_line = []

		for point in range(len(raw_data)-1):
			scan_line.append([raw_data[point][ANGLE_INDEX],raw_data[point][RADIUS_INDEX]])
			if raw_data[point][STEP_INDEX] != raw_data[point+1][STEP_INDEX]:
				scans.append(scan_line)
				scan_line = []
		scans.append(scan_line)
	return scans

def process_scans(scans):
	processed = [] 
	for scan in range(len(scans)):
		point_cloud = []
		for point in range(len(scans[scan])):
			angle = np.radians(float(scans[scan][point][0]))
			radius = float(scans[scan][point][1])
			x = np.cos(angle)*radius
			y = np.sin(angle)*radius
			p = [x,y,0.0]
			new_point = pr.Rotate(p, [0,1,0], [0,0,0], np.radians(30))
			new_point[0] += X_OFFSET
			new_point[2] += Z_OFFSET
			absolute_point = pr.Rotate(new_point, [0,0,0], [0,0,1], np.radians(scan*1.8))
			point_cloud.append(absolute_point)	
		processed.append(point_cloud)
	return processed

def filter_scans(scans):
	processed = [] 
	for scan in range(len(scans)):
		point_cloud = []
		for point in range(len(scans[scan])):
			angle = np.radians(float(scans[scan][point][0]))
			radius = float(scans[scan][point][1])
			if radius >= 1000:
				x = np.cos(angle)*radius
				y = np.sin(angle)*radius
				p = [x,y,0.0]
				new_point = pr.Rotate(p, [0,1,0], [0,0,0], np.radians(30))
				new_point[0] += X_OFFSET
				new_point[2] += Z_OFFSET
				absolute_point = pr.Rotate(new_point, [0,0,0], [0,0,1], np.radians(scan*1.8))
				point_cloud.append(absolute_point)	
		processed.append(point_cloud)
	return processed

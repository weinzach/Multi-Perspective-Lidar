import numpy as np

def lidarRead(file):
    with open(file, 'r') as f:
        rawData  = []
        rawCloud =[]
        scans = []
        index = 0
        i = 0
        for line in f:
            rawData.append(line.rstrip().split('\t'))
            #
            rawCloud.append([rawData[i][2], rawData[i][3], rawData[i][4]])
            print(rawData[i][3])
            i +=1    
        
        scanLine = []
        
        for point in range(len(rawData)):
            scanLine.append([rawCloud[point][0],rawCloud[point][1]])
            if rawData[point][0] == 'True':
                scans.append(scanLine)
                scanLine = []
    return scans    

def processScan(data):      
    scans = []
    for scan in range(len(data)):
        
        pointCloud = []
        for point in range(len(data[scan])):  
            rval = float(data[scan][point][1])
            thval = np.radians(float(data[scan][point][0]))
            x = (np.cos(thval)*rval)
            y = (np.sin(thval)*rval)
            p = [x,y,0.0]
            pointCloud.append(p)
        
        scans.append(pointCloud)
    
    return scans
            

            
    
        
                
                
    

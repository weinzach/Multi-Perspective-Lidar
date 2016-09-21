import numpy as np
from math import sin, cos, pi

def R(theta, u):
    return [[cos(theta) + u[0]**2 * (1-cos(theta)), 
             u[0] * u[1] * (1-cos(theta)) - u[2] * sin(theta), 
             u[0] * u[2] * (1 - cos(theta)) + u[1] * sin(theta)],
            [u[0] * u[1] * (1-cos(theta)) + u[2] * sin(theta),
             cos(theta) + u[1]**2 * (1-cos(theta)),
             u[1] * u[2] * (1 - cos(theta)) - u[0] * sin(theta)],
            [u[0] * u[2] * (1-cos(theta)) - u[1] * sin(theta),
             u[1] * u[2] * (1-cos(theta)) + u[0] * sin(theta),
             cos(theta) + u[2]**2 * (1-cos(theta))]]

def Rotate(pointToRotate, point1, point2, theta):


    u= []
    squaredSum = 0
    for i,f in zip(point1, point2):
        u.append(f-i)
        squaredSum += (f-i) **2

    u = [i/squaredSum for i in u]
    r = R(theta, u)
    rotated = []

    for i in range(3):
        rotated.append(round(sum([r[j][i] * pointToRotate[j] for j in range(3)])))

    return rotated

def rotateCloud(pointCloud, point1, point2, theta):
    newCloud = []
    for point in range(len(pointCloud)):
        inPoint = [pointCloud[point][0], pointCloud[point][1], pointCloud[point][2]]
        outPoint = Rotate(inPoint, point1, point2, theta)
        newCloud.append(outPoint)
    
    return newCloud
    
def acquirePoints(pointCloud):
    xs = []
    ys = []
    zs = []
    for point in range(len(pointCloud)):
        xs.append(pointCloud[point][0])
        ys.append(pointCloud[point][1])
        zs.append(pointCloud[point][2])
    return xs,ys,zs

def initialRotation(pointCloud):
    return rotateCloud(pointCloud, [0,1,0], [0,0,0], np.radians(30))
    
def initialOffset(pointCloud):
    for point in pointCloud:
        point[0] += 60
        point[2] += 25
        


        
    

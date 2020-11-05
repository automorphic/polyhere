import svgwrite
import math
import random
from svgwrite import cm, mm  

# draw box of size (width, height) with center (x,y) 
def draw_box(d, width, height, x, y):
    box = d.add(d.g(id='box', stroke='blue'))
    p = width / 2
    q = height / 2
    box.add(d.line(start=((x-p)*cm, (y+q)*cm), end=((x+p)*cm, (y+q)*cm)))
    box.add(d.line(start=((x+p)*cm, (y+q)*cm), end=((x+p)*cm, (y-q)*cm)))
    box.add(d.line(start=((x+p)*cm, (y-q)*cm), end=((x-p)*cm, (y-q)*cm)))
    box.add(d.line(start=((x-p)*cm, (y-q)*cm), end=((x-p)*cm, (y+q)*cm)))

# draw hexagon of radius 'size' with center x,y
def draw_hexagon(d, x, y, size):
    hex = d.add(d.g(id='hex', stroke='blue'))
    p = size / 2
    q = size * math.sqrt(3) / 2
    
    hex.add(d.line(start=((x-p)*cm, (y+q)*cm), end=((x+p)*cm, (y+q)*cm)))
    hex.add(d.line(start=((x+p)*cm, (y+q)*cm), end=((x+2*p)*cm, (y)*cm)))
    hex.add(d.line(start=((x+2*p)*cm, (y)*cm), end=((x+p)*cm, (y-q)*cm)))
    hex.add(d.line(start=((x+p)*cm, (y-q)*cm), end=((x-p)*cm, (y-q)*cm)))
    hex.add(d.line(start=((x-p)*cm, (y-q)*cm), end=((x-2*p)*cm, (y)*cm)))
    hex.add(d.line(start=((x-2*p)*cm, (y)*cm), end=((x-p)*cm, (y+q)*cm)))

# given a circle with center (x, y) and radius r
# return the coordinates of n points on the circle
def calc_radialpoints(x, y, numpoints, rad, phase):
    result = []
    
    theta = 2*math.pi / numpoints
    
    for i in range(numpoints):
        radialpoint = (x + rad*math.cos(theta*i + phase), y + rad*math.sin(theta*i + phase))
        result.append(radialpoint)

    return result

# given an array of coordinates, draws a polygon
def draw_poly(d, points):
    poly = d.add(d.g(id='poly', stroke='blue'))
    
    for i in range(len(points)):
        if (i == len(points) - 1):
            startPoint = points[i]
            endPoint = points[0]            
        else:
            startPoint = points[i]
            endPoint = points[i+1]
        
        poly.add(d.line(start=(startPoint[0]*cm,startPoint[1]*cm), end=(endPoint[0]*cm, endPoint[1]*cm)))
       
def draw_polyset(d, x, y, num, dist, size, poly_sides, phase, phase_sec): 
    pts = calc_radialpoints(x, y, num, dist, phase)
    
    for i in range(len(pts)):
        polyPtCenter = pts[i]
        polyPts = calc_radialpoints(polyPtCenter[0], polyPtCenter[1], poly_sides, size, phase_sec)
        draw_poly(d, polyPts)
 
f = 'result.svg'

# frame dimensions
dimX = 93.98       # width of the frame
dimY = 63.5        # height of the frame
borderSize = 20.32 # cumulative thickness of the borders

baseSize = 3       # length of polygon side in initial polygon(s)
reduceRatio = 1.13  # ratio by which polygon size is reduced in subsequent iteration
baseScale = 2.3      # scale factor to control "expansiveness"
baseAdd = baseSize / baseScale  # initial amount of space to add  between seeded polygons
baseExpand = baseSize + baseAdd # distance between frame center and center of each drawn polygon
numPoly = 8        # number of polygons to draw 
multiplier = 1.28     # multiplier for number of polygons in each successive iteration
maxLevel = 12       # number of iterations
polySides = 6      # number of sides in each polygon

if __name__ == '__main__':
    
    
    dwg = svgwrite.Drawing(filename=f, debug=True)
 
   # calculate the center    
    cenX = dimX / 2
    cenY = dimY / 2
    draw_box(dwg, dimX, dimY, cenX, cenY)
    draw_box(dwg, dimX - borderSize, dimY - borderSize, cenX, cenY)
    
    # seed the initial drawing
    for i in range(maxLevel):    
        phase1 = math.pi*random.randint(0,180)/180 # first order phase
        phase2 = math.pi*random.randint(0,180)/180 # second order phase
        draw_polyset(dwg, cenX, cenY, numPoly, baseExpand, baseSize, polySides, phase1, phase2)    
        numPoly = int(round(numPoly * multiplier, 0))
        baseExpand = baseExpand + baseScale*baseSize   
        baseSize = baseSize / reduceRatio
    dwg.save()
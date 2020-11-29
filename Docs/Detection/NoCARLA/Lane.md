# Lane Detection
[Docs][docs-url] -> [Detection][detection-path] -> [Detection without CARLA][detection-no-carla] -> Lane Detection

&nbsp;&nbsp;&nbsp;&nbsp; In this section we provide a description of the steps taken to reach our final implementation of the lane detection using a Spatial CNN. To integrate this service in our pipeline we followed [this guide][lane-detection-guide]

## Contents
1.  [First Approach: Hough Transform](#Hough-Transform)  
    1.1. Edge Detection
2.  Second Approach: SCNN

## Hough Transform

&nbsp;&nbsp;&nbsp;&nbsp; The main objective ot the Hough Transform method is to **identify straight lines**, this method would later be improved to work with other shapes, however we only implemented its first version.

&nbsp;&nbsp;&nbsp;&nbsp; Since most of the times, a lane would be a straight line we decided this method would be a suitable option to perform lane detection. For this method to work the images should be **binary** but, since we need to search for lines in the color space we first must **apply a grayscale filter** tp the image, after that we can then perform other CV methods to detect edges (in our case we applied a Sobel filter).


&nbsp;&nbsp;&nbsp;&nbsp; A straight line can be represented as a tuple (a,b) where a is its slope and b its intercept, this is also true for the polar space, where a line can be represented by the tuple <img src="https://latex.codecogs.com/gif.latex?(\rho&space;,\theta&space;)" title="(\rho ,\theta )" /> where <img src="https://latex.codecogs.com/gif.latex?\rho" title="\rho" />  is the shortest distance from the origin point to the line and <img src="https://latex.codecogs.com/gif.latex?\theta" title="\theta" /> is the angle between the x-axis and the distance line. Using the polar space we can then describe all types of line orientations.

![Line with polar space relation][polar-space-line]

For this specific image its equation is as follows for every x,y point: 

<img src="https://latex.codecogs.com/gif.latex?\rho&space;=&space;x&space;cos(\theta&space;)&space;&plus;&space;ysin(\theta&space;)" title="\rho = x cos(\theta ) + ysin(\theta )" />  

<br>

The <img src="https://latex.codecogs.com/gif.latex?(\rho&space;,\theta&space;)" title="(\rho ,\theta )" /> representation allows us to represent the line as a **point in the Hough Space**

![Line representation in the Hough Space][polar-space-hough]

&nbsp;&nbsp;&nbsp;&nbsp; Considering a complex enough image if we pick a point in the cartesian coordinate system it is very probable that many lines pass through that point where each line would have different (a,b) parameters and that would result in several points in the Hough Space. We can now find am equation to describe all these points. Continuously adding more intersecting lines would result in a sinusoid in the Hough Space. So we reach the following conclusion, **for a fixed (x,y) parameters representing a point in an image, if we consider all the possible values/orientation of <img src="https://latex.codecogs.com/gif.latex?\theta" title="\theta" /> in a certain range we obtain <img src="https://latex.codecogs.com/gif.latex?\rho" title="\rho" /> values forming a sinusoid.

![Point representation of all its values, forming a sinusoid][hough-sinusoid]


&nbsp;&nbsp;&nbsp;&nbsp; All this theory may sound confusing but its the foundation to finding lines in a matrix of pixels. If we draw several points, forming a line, or a lane, in the image space we observe that we obtain a bunch of sinusoids in the Hough space **all intersecting at one point**.

![Hough representation of points forming a line in the image space][hough-sinusoid-intersect]

&nbsp;&nbsp;&nbsp;&nbsp; This proves crucial in our task since, to find a straight line, we should **find intersections in the Hough space**


[docs-url]: ../../../README.md
[detection-path]: ../
[detection-no-carla]: Detection.md
[lane-detection-guide]: https://towardsdatascience.com/tutorial-build-a-lane-detector-679fd8953132#bbac
[polar-space-line]: ../../Images/Lane/polar_line.jpg
[polar-space-hough]: ../../Images/Lane/polar_hough.jpg
[hough-sinusoid]: ../../Images/Lane/hough_sinusoid.jpg
[hough-sinusoid-intersect]: ../../Images/Lane/hough_intersect_lines.jpg
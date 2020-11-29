# Lane Detection
[Docs][docs-url] -> [Detection][detection-path] -> [Detection without CARLA][detection-no-carla] -> Lane Detection

&nbsp;&nbsp;&nbsp;&nbsp; In this section we provide a description of the steps taken to reach our final implementation of the lane detection using a Spatial CNN. To integrate this service in our pipeline we followed [this guide][lane-detection-guide]

## Contents
1.  [First Approach: Hough Transform](#Hough-Transform)  
    1.1. [Edge Detection Pipeline](#Edge-Detection-Pipeline)  
    1.2. [Gray Scale](#Gray-Scale)  
    1.3. [Gaussian Filter](#Gaussian-Filter)  
    1.4. [Sobel filter](#Sobel-filter)  
    1.5. [Non-Maximum Suppression](#Non-Maximum-Suppression)   
    1.6. [Hysteresis thresholding](#Hysteresis-thresholding)   
    1.7. [Canny Detector Results](#Canny-Detector-Results)
2.  Second Approach: SCNN

# Hough Transform

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

&nbsp;&nbsp;&nbsp;&nbsp; This proves crucial in our task since, to find a straight line, we should **find intersections in the Hough space**.


<br><br><br>

## Edge Detection Pipeline
&nbsp;&nbsp;&nbsp;&nbsp; So we've already found a way of finding lines through the Hough space, to do so, the image needs to be binary, so we need to first **convert it to grayscale**. Since we are interested in lines it makes no sense in keeping any other info in the image, as such, we will apply an edge detection algorithm, we choose the **Canny edge detector** which is a multi-stage algorithm optimized for fast real-time edge detection and has the following steps:

+   Apply a **Gaussian filter** to smooth the image in order to remove noise
+   Find the intensity gradients of the image to detect orientation of edges through a Sobel filter
+   Apply a non-maximum suppression algorithm to sharpen the edges
+   Perform Hysteresis thresholding to analyse less intensive pixels
<br><br><br>

## Gray Scale
&nbsp;&nbsp;&nbsp;&nbsp; Since methods to convert an image to grayscale may vary we followed one type, found on [Wikipedia][gray-url] where we calculate a *nonlinear Luma component directly from gamma-compressed primary intensities as a weighted sum*

![Image after applying Gray Scale][gray-img]

<br><br><br>

## Gaussian Filter
&nbsp;&nbsp;&nbsp;&nbsp; The Gaussian filter (smoothing operator) is a 2D **[convolution][convolution-url] operator** used to blur/smooth images and remove noise similar to the [mean][mean-url] filter but using a different [kernel][kernel-url] representing the shape of a Gaussian curve and can be calculated as follows (assuming a normal distribution):

<img src="https://latex.codecogs.com/gif.latex?G&space;=&space;\frac{1}{\sqrt{2\pi&space;}\sigma&space;}e^{-\frac{x^{2}}{2\sigma^{2}}}&space;$&space;$;\sigma$&space;$&space;is$&space;$the$&space;$&space;standard$&space;$&space;deviation&space;$&space;$of$&space;$&space;the$&space;$&space;distribution" title="G = \frac{1}{\sqrt{2\pi }\sigma }e^{-\frac{x^{2}}{2\sigma^{2}}} $ $;\sigma$ $ is$ $the$ $ standard$ $ deviation $ $of$ $ the$ $ distribution" />


&nbsp;&nbsp;&nbsp;&nbsp; The main idea is to use the distribution as a point-spread function through convolution.

<br><br><br>

## Sobel filter

&nbsp;&nbsp;&nbsp;&nbsp; The Sobel operator is an **approximation to a derivative of an image** separated in the x and y axis. We use a 3x3 kernel one dim for each x and y direction. The x-gradient has negative values on the left side (before the middle column) and positive numbers on the right side, the center is 0. The y-gradient has negative numbers on the bottom and positive on top. The Sobel operator tries to find the **amount of difference by placing the gradient matrix over each pixel of the image**.

![Sobel Gradients][sobel-kernel]
<br><br><br>

## Non-Maximum Suppression
&nbsp;&nbsp;&nbsp;&nbsp; This step will essentially sharpen the edges where, for each pixel we will check of its value is a local minimum in which case we test for the next pixel otherwise it is set to 0/suppressed.

<br><br><br>

## Hysteresis thresholding

&nbsp;&nbsp;&nbsp;&nbsp; Here, we will simply apply a threshold filter to lower intensity pixels to see if they represent an edge or noise, if the pixel has an intensity gradient higher than our upper limit, it is an edge if it is lower than the lower limit it is discarded. For pixels within the threshold if the adjacent pixels are above the upper limit they too are considered edges, otherwise they are discarded.

<br><br><br>

## Canny Detector Results
We now present the results of applying the canny edge detector to an image (applying the gray scale and gaussian filters before).

<br>
Original image

![Original image][original-img]


Canny edge detection:

![Canny image][canny-img]

<br><br><br>

## Segmentation
&nbsp;&nbsp;&nbsp;&nbsp; Since all we want to do is detect lanes, lines on the lower portion of our image we don't need all the other values, as such we wil segment them. The following image shows what we want to consider

![Segment Objective][segment-objective]


Looking at an original image segmented:

![Segmented original image][segement-origial]

And the segmented Canny:

![Segmented Canny][segment-canny]







[docs-url]: ../../../README.md
[detection-path]: ../
[detection-no-carla]: Detection.md
[lane-detection-guide]: https://towardsdatascience.com/tutorial-build-a-lane-detector-679fd8953132#bbac
[polar-space-line]: ../../Images/Lane/polar_line.jpg
[polar-space-hough]: ../../Images/Lane/polar_hough.jpg
[hough-sinusoid]: ../../Images/Lane/hough_sinusoid.jpg
[hough-sinusoid-intersect]: ../../Images/Lane/hough_intersect_lines.jpg
[gray-url]: https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale
[gray-img]: ../../Images/Lane/gray.jpg
[convolution-url]: https://homepages.inf.ed.ac.uk/rbf/HIPR2/convolve.htm
[mean-url]: https://homepages.inf.ed.ac.uk/rbf/HIPR2/mean.htm
[kernel-url]: https://homepages.inf.ed.ac.uk/rbf/HIPR2/kernel.htm
[sobel-kernel]: ../../Images/Lane/sobel_kernel.jpg
[original-img]: ../../Images/Lane/original.jpg
[canny-img]: ../../Images/Lane/canny.jpg
[segment-objective]: ../../Images/Lane/segment_objective.jpg
[segement-origial]: ../../Images/Lane/segment_original.jpg
[segment-canny]: ../../Images/Lane/segment_canny.jpg
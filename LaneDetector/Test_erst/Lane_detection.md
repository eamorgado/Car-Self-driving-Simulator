# Lane detection notes
Canny detection algorithm:
Step 1 - Convert image to grayscale
Step 2 - Reduce noise with Gaussian filter (Gaussian Blur)
Step 3 - Apply Canny function
Step 4 - Segmentation (Region of interest)
Step 5 - Hough trasform

## Importing images
Python has at least 4 libraries to import images. A good summary  and comparation regarding computational time can be found here:

https://towardsdatascience.com/what-library-can-load-image-in-python-and-what-are-their-difference-d1628c6623ad

**Important**: OpenCV (cv2) imports images as BGR. The orher ones as RGB. Note also that matplotlib imports as RGBa (the images has four layeers (Red, Green, Blue and alpha [alpha is opacity])).

## Grayscale (Step1)

Usually the Python libraries uses the following expression to convert from RGB to grayscale:
$$ gray = 0.2898 \times R + 0.5870 \times G + 0.1140 \times B $$

Note that there are other ways to obtain a grayscale image. For instance, one can just comput the mean of R, G and B:
$$ gray = \frac{R+G+B}{3}$$

**Important**: to plot a grayscale image using pyplot form matplotlib, the following should be made:

plt.imshow(gray_image, cmap=plt.get_cmap('gray'))

## Gaussian Blur (Step 2)
**Important**: The function cv2.Canny by default applies internely the 5 by 5 gaussian.

## Canny function (Step 3)
Detection of the edges by differentiation.

**Thresholds**
If the grandient is larger than the upper threshold then it is accepted as an edge pixel. If it is below the lower threshold it is rejected. If the gradient is between the threshold then it will be accepted only if it is connected to a strong edge.
The documentation recomends to use a ratio of 1 to 2 or 1 to 3. For instance, ratio of 1 to 3 is 50 to 150

cv2.Canny(blur_image or grey_image, threshold1=50, threshold2=150)

## Segmentation - Region of interest (Step 4)
Everything outside the polygon will have zeros (black). Basically, the polygon defines the lane right lane of the road.

We are going to use the mask to only show a specific portion of the image. Everything else we want to mask. Therefore, we only show the region of interest traced by the triangular polygon. 
Using the bitwise operation (&) we will stay only with the region defined by the triangle.

## Hough transform (Step 5)

lines = cv2.HoughLinesP(cropped_image, 
                        rho=2, # precision 2 of pixels 
                        theta=np.pi/180, # 1 degree per pixel
                        threshold=100, # Minumum number of intersections in the bin to be considered a relevant line
                        lines=np.array([]), # holder array
                        minLineLength=40, # length of the line (a line with less 40 pixels is rejected)
                        maxLineGap=5)     # Maximum distance in pixels between segmented lines which we will allow to be connected.

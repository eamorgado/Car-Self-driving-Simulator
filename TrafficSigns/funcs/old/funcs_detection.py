import imutils

def sliding_window(image, step, ws):
    '''
    image - input image
    step - step size of the sliding (it is common to use steps of 4 to 8 pixels)
    ws - window size. Defines the width and height (in pixels) of the window we are going to extract from the image
    '''
    # slide a window across the image
    for y in range(0,image.shape[0] - ws[1], step): # loop over rows
        for x in range(0, image.shape[1] - ws[0], step): # loop over columns
            # yield the current window
            yield (x, y, image[y:y + ws[1], x:x + ws[0]])


def pyramid(image, scale=1.5, minSize=(30, 30)):
    '''
    image - input image
    scale - controls by how much the image is resized at each layer
    minSize - is the minimum required width and height of the layer. If an image in the pyramid falls below this minSize, the construction of the pyramid is stopped.
    '''
    # yield the original image
    yield image
    
    #keep looping over the pyramid
    while True:
        # keep looping over new dimensions of the image and resize it
        w = int(image.shape[1]/scale)
        image = imutils.resize(image, width=w)
        
        # if the resized image does not meet the supplied minimum
        # size, then stop constructin the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
            
        # yield the next image in the pyramid
        yield image
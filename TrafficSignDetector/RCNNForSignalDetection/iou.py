# Function to calculate IOU (Intersection Over Union)

def compute_iou(boxA, boxB):
    assert boxA[0] < boxA[2]
    assert boxA[1] < boxA[3]
    assert boxB[0] < boxB[2]
    assert boxB[1] < boxB[3]

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
	# rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	
    # compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the intersection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
	
    # return the intersection over union value
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

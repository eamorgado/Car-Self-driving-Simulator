# import the necessary packages
import os

# define the base path to the *original* input dataset and then use
# the base path to derive the image and annotations directories
ORIG_BASE_PATH = "./dataset"
ORIG_IMAGES = ORIG_BASE_PATH #os.path.sep.join([ORIG_BASE_PATH, "images"])
ORIG_ANNOTS = os.path.sep.join([ORIG_BASE_PATH, "gt.txt"])

# define the base path to the *new* dataset after running our dataset
# builder scripts and then use the base path to derive the paths to
# our output class label directories
BASE_PATH = "/mnt/c/Users/Eduardo/Desktop/SP/MIERSI/4A/1S/VC/dataset"
POSITIVE_CLASS = 'signal'
NEGATIVE_CLASS = 'no_signal'
POSITIVE_PATH = os.path.sep.join([BASE_PATH, POSITIVE_CLASS]) # positive (there is a raccoon)
NEGATIVE_PATH = os.path.sep.join([BASE_PATH, NEGATIVE_CLASS]) # negative (no raccoon in the input image)

# define the number of max proposals used when running selective
# search for (1) gathering training data and (2) performing inference
MAX_PROPOSALS = 2000
MAX_PROPOSALS_INFER = 200

# define the maximum number of positive and negative images to be
# generated from each image
MAX_POSITIVE = 30
MAX_NEGATIVE = 10

# initialize the input dimensions to the network
INPUT_DIMS = (224, 224)

# define the path to the output model and label binarizer
MODEL_PATH = "./data/model.h5"
ENCODER_PATH = "./data/label_map.pickle"

# define the minimum probability required for a positive prediction
# (used to filter out false-positive predictions)
MIN_PROBA = 0.7

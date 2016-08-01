from pybrain.tools.customxml import NetworkReader
from PIL import Image

def flatten(image):
    """
    take a PIL Image and return a 1D array of grayscale values, used by loadImage()
    """
    w,h = image.size
    px = image.load()
    
    result = []
    for y in range(32):
        for x in range(32):
            try:
                value = px[x,y]
                value /= 255.0
            except IndexError:
                value = 0.0
            result.append(value)
    return result
def loadImage(fpath):
    """
    load an image from a filename and return a 1D array of values 0-1 representing grayscale average
    
    Example:
        >>> im = loadImage('path/to/image.png')
        >>> print im
        [0.02,0.932,0.2...]
    """
    im = Image.open(fpath).convert('L')
    return flatten(im)
def classify(data,network_file='network_training_progress.xml'):
    """
    Takes two arguments, 'data' is a 1D array of floats ranging 0-1 representing grayscale values of an image,
    'network_file' is an xml file output from 'pybrain_playground.py', a pre-trained network. 
    Returns two floats, how much it guesses that a given input is a track or other, respectively.
    Again, classify()[0] is chances it is a track, classify()[1] is chances it is other. Ranged 0-1.
    
    Example:
        >>> im = loadImage('path/to/track.png')
        >>> print classify(im)[0]
        0.99
        >>> print classify(im)[1]
        0.01
    Here, 0.99 indicates it believes with 99% certainty that the image is a track, 
    and 0.01% certainty that it is not a track.
    
    """
    net = NetworkReader.readFrom(network_file)
    return net.activate(data)
    
    
im = loadImage('/Users/cisnerosa/Documents/WIPAC/Scripts/ANN/training_data/signal_sample/2013.02.21-101776098_medium.png')
print classify(im)
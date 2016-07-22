import os

from pybrain.datasets                import ClassificationDataSet
from pybrain.utilities               import percentError
from pybrain.tools.shortcuts         import buildNetwork
from pybrain.supervised.trainers     import BackpropTrainer
from pybrain.structure.modules       import SoftmaxLayer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader

class SignalClassifier(object):
    total_epochs = 0
    in_file = None
    out_file = os.path.join(os.getcwd(),'network_data.xml')
    
    def __init__(self,in_file=None,out_file=None):
        pass
    def makeOneDimensional(self,array):
        result = []
        for (y,row) in enumerate(image):
            for (x,value) in enumerate(row):
                result.append(array[y][x])
        return result
c = SignalClassifier()
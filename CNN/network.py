import os

from pybrain.datasets                import ClassificationDataSet
from pybrain.utilities               import percentError
from pybrain.tools.shortcuts         import buildNetwork
from pybrain.supervised.trainers     import BackpropTrainer
from pybrain.structure.modules       import SoftmaxLayer

#from pybrain.tools.xml.networkwriter import NetworkWriter
#from pybrain.tools.xml.networkreader import NetworkReader

class SignalClassifier(object):
    total_epochs = 0
    in_file = None
    out_file = os.path.join(os.getcwd(),'network_data.xml')
    
    def __init__(self,in_file=None,out_file=None):
        if in_file != None:
            self.in_file = in_file
        if out_file != None:
            self.out_file = out_file
        
        if self.in_file == None:
            pass
    def epoch(self):
        #epoch
        #self.total_epochs += 1
        return NotImplemented
    def createState(self):
        pass
    def saveState(self):
        pass
       # NetworkWriter.write(self.out_file)
    def loadState(self):
        pass
    def makeOneDimensional(self,array):
        result = []
        for (y,row) in enumerate(image):
            for (x,value) in enumerate(row):
                result.append(array[y][x])
        return result
c = SignalClassifier()
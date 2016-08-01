#http://www.pybrain.org/docs/
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SigmoidLayer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.datasets import ClassificationDataSet
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader
from pybrain.tools.shortcuts import buildNetwork

from pybrain.utilities import percentError
from pybrain.structure import TanhLayer
from matplotlib import pyplot as plt

from time import time
from PIL import Image
import numpy as np
import resource
import math 
import sys
import os

def flatten(image):
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
    im = Image.open(fpath).convert('L')
    return flatten(im)
def loadFolder(fpath):
    results = []
    for (dname,dirnames,fnames) in os.walk(fpath):
        for fname in fnames:
            if fname[-4:] != '.png':
                continue
            results.append(loadImage(os.path.join(fpath,fname)))
    return results
def fill_dataset(ds,data,value):
    for point in data:
        ds.appendLinked(point,[value])
    return ds
def add_arrs(arrays):
    #takes a tuple or list of two arrays of equal length, and adds them
    result = []
    for (index,value) in enumerate(arrays[0]):
        value2 = arrays[1][index]
        result.append(0 if value2 + value == 1 else 1)
    return result
def retrieve_names():
    paths = [
        '/users/cisnerosa/documents/wipac/scripts/cnn/training_data/signal_sample/',
        '/users/cisnerosa/documents/wipac/scripts/cnn/training_data/noise_sample/',
    ]
    results = []
    for p in paths:
        for (dname,dnames,fnames) in os.walk(p):
            for f in fnames:
                if f[-4:] != '.png':
                    continue
                results.append(f)
    return results
def retrieve_score(name,category='Track'):
    with open('results.txt') as rfile:
        lines = rfile.readlines()
        amount = eval(lines[0])
        results = eval('\n'.join(lines[1:]))
        return results[name][category]
        
#load 1003 32x32 images....yeesh, I should do something about that. Coincidentally it's almost 1024x1024 (32x32 is 1024)
signal_training_pth = '/users/cisnerosa/documents/wipac/scripts/cnn/training_data/signal_sample/'
signal_training_data = loadFolder(signal_training_pth)

noise_training_pth = '/users/cisnerosa/documents/wipac/scripts/cnn/training_data/noise_sample/'
noise_training_data = loadFolder(noise_training_pth)

signal_test_pth = '/users/cisnerosa/documents/wipac/scripts/cnn/validation_data/signal_sample/'
signal_test_data = loadFolder(signal_test_pth)

noise_test_pth = '/users/cisnerosa/documents/wipac/scripts/cnn/validation_data/noise_sample/'
noise_test_data = loadFolder(noise_test_pth)

#training dataset fill training dataset with training data, 0 and 1 correspond to the index of ['Track','Other'] 

trn_dataset = ClassificationDataSet(1024,nb_classes=2,class_labels=['Track','Other'])#both datasets

trn_dataset = fill_dataset(trn_dataset,signal_training_data,0)
trn_dataset = fill_dataset(trn_dataset,noise_training_data,1)

#test dataset
test_dataset = ClassificationDataSet(1024,nb_classes=2,class_labels=['Track','Other'])
test_dataset = fill_dataset(test_dataset,signal_test_data,0)
test_dataset = fill_dataset(test_dataset,noise_test_data,1)

combined_data = ClassificationDataSet(1024,nb_classes=2,class_labels=['Track','Other'])
combined_data = fill_dataset(combined_data,signal_training_data,0)
combined_data = fill_dataset(combined_data,signal_test_data,0)
combined_data = fill_dataset(combined_data,noise_training_data,1)
combined_data = fill_dataset(combined_data,noise_test_data,1)

#optimization
trn_dataset._convertToOneOfMany()
test_dataset._convertToOneOfMany()

#1024 inputs (flattened 32x32 image), 32 hidden neurons, 2 outputs
net = buildNetwork(trn_dataset.indim, 16,64,2, trn_dataset.outdim,hiddenclass=TanhLayer,outclass=SoftmaxLayer,bias=True)
#net = NetworkReader.readFrom('/users/cisnerosa/desktop/network_training_progress.xml')
trainer = BackpropTrainer(net, dataset=trn_dataset, momentum=0.01, weightdecay=0.01,learningrate=0.01)

start = time()

#e = 10
EPOCHS = 600
train_err = []
test_err = []
while trainer.totalepochs < EPOCHS:
   trnresult = percentError(trainer.testOnClassData(dataset=trn_dataset), trn_dataset['class'])
   tstresult = percentError(trainer.testOnClassData(dataset=test_dataset), test_dataset['class'])
   print 'trn: {}%, test: {}%| epochs: {}'.format(str(100-trnresult)[:5],str(100-tstresult)[:5],trainer.totalepochs)
   train_err.append(trnresult)
   test_err.append(tstresult)
   
   trainer.train()
   
#trainer.trainOnDataset(trn_dataset,EPOCHS)


best = min(test_err)
index = len(test_err)-1-test_err[::-1].index(best)
elapsed = time() - start

print 'lowest: {}% accuracy (epoch {})'.format(100-int(best),index)


plt.plot(train_err,'b',test_err,'r')
plt.plot([0,len(test_err)],[best,best],'g')
plt.annotate('{}%err ({}% accuracy) - epoch {}'.format(int(best),100-int(best),index),xy=[index,best],xytext=[len(test_err)/2+15,best+15],arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()



results = trainer.testOnClassData(combined_data,return_targets=True)
comparison = add_arrs(results)
print comparison.count(1), " correct; ", comparison.count(0), " incorrect"
#print comparison
#names = retrieve_names()
#for (index,c) in enumerate(comparison):
   # print '{} : {}'.format(names[index],'correct' if c == 1 else 'incorrect')
#print results

print '{} hours {} minutes {} seconds ({} elapsed)'.format(int(math.floor(elapsed / 3600)),int(math.floor((elapsed / 60) % 60)),int(math.floor(elapsed % 60)),elapsed)
NetworkWriter.writeToFile(net, '/users/cisnerosa/desktop/network_training_progress.xml')


print "epoch: %4d" % trainer.totalepochs#, "  train error: %5.2f%%" % trnresult, "  test error: %5.2f%%" % tstresult
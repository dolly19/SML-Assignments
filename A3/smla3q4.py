# -*- coding: utf-8 -*-
"""SMLA3Q4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iEkGxpSoT268ylEn7VfL5BXsD6IQ8zED
"""

!pip install -q idx2numpy

from google.colab import drive
drive.mount('/content/gdrive')

import pandas as pd
import idx2numpy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix

#loading the dataset
X_train = idx2numpy.convert_from_file('/content/gdrive/MyDrive/ML datasets/SML/mnist/train-images.idx3-ubyte')
y_train = idx2numpy.convert_from_file('/content/gdrive/MyDrive/ML datasets/SML/mnist/train-labels.idx1-ubyte')
X_test = idx2numpy.convert_from_file('/content/gdrive/MyDrive/ML datasets/SML/mnist/t10k-images.idx3-ubyte')
y_test = idx2numpy.convert_from_file('/content/gdrive/MyDrive/ML datasets/SML/mnist/t10k-labels.idx1-ubyte')

#Reshaping the data from 3d to 2d
X_train = X_train.reshape(len(X_train),X_train.shape[1]*X_train.shape[2])
X_test = X_test.reshape(len(X_test),X_test.shape[1]*X_test.shape[2])

#Applying PCA for the best value reported in question-2 i.e n_components = 15
pca_15 = PCA(n_components = 15)
pca_15.fit(X_train)
X_train = pca_15.transform(X_train)
X_test = pca_15.transform(X_test)

#implemented FDA function
def FDA(X,Y):
  n_rows,n_cols = X.shape
  St = np.matmul((X - np.mean(X)).T,(X-np.mean(X)))
  Sw = np.zeros((n_cols,n_cols))
  number_classes = np.max(Y)
  for ith_class in range(number_classes+1):
    Xc = X[Y==ith_class,: ]
    Sw = Sw + np.matmul((Xc-np.mean(Xc)).T,(Xc-np.mean(Xc)))
  Sw = Sw + np.matmul((Xc-np.mean(Xc)).T,Xc-np.mean(Xc))
  w,v = np.linalg.eigh(np.matmul(np.linalg.inv(Sw),(St-Sw)))
  W = []
  for temp,w in sorted(zip(w,v),reverse = True):
    W.append(np.array(w))
  W = np.array(W[:number_classes])
  #print(W)
  return W

#coefficent vector
W = (FDA(X_train,y_train))

lda = LinearDiscriminantAnalysis()

#projecting training data using W for both training and testing data
Y_train_t = np.matmul(X_train,W.T)
Y_test_t = np.matmul(X_test,W.T)

#applying LDA on the projected data Y for classifying the testing samples
lda.fit(Y_train_t,y_train)

#accuracy
print("Accuracy ", lda.score(Y_test_t,y_test))

#class-wise accuracy for testing dataset
y_pred = lda.predict(Y_test_t)
CM = confusion_matrix(y_test,y_pred)

n = len(CM)
print("Class-wise accuracy")
for i in range(n):
  s = CM[i].sum()
  accuracy = CM[i][i]/s
  print("Label",i," - ",accuracy)
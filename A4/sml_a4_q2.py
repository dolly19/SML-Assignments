# -*- coding: utf-8 -*-
"""SML_A4_Q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AH5Wwczsf8wYOxDd4e6SDSv_rps9rkOZ
"""

from google.colab import drive
drive.mount('/content/gdrive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from tqdm import tqdm
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.initializers import RandomNormal
from tensorflow.keras.initializers import Zeros

"""#Question 2

## Feed forward Neural Network
"""

#loading the dataset
train = pd.read_csv('/content/gdrive/MyDrive/ML datasets/SML/fminst/fashion-mnist_train.csv')
test = pd.read_csv('/content/gdrive/MyDrive/ML datasets/SML/fminst/fashion-mnist_test.csv')

#splitting into features and label
X_train = train[train.columns[1:]].to_numpy()
y_train = train['label'].to_numpy()
X_test = test[test.columns[1:]].to_numpy()
y_test = test['label'].to_numpy()

X_train.shape

#applying oneHotEncoding
y_train_en = pd.get_dummies(y_train).to_numpy()
y_test_en = pd.get_dummies(y_test).to_numpy()

# defining the 784-256-128-10 architecture using Keras
model = Sequential()
model.add(Dense(256, input_shape=(784,), activation="sigmoid",kernel_initializer='random_normal',
    bias_initializer='zeros'))
model.add(Dropout(0.3))
model.add(Dense(128, activation="sigmoid"))
model.add(Dropout(0.3))
model.add(Dense(10, activation="softmax"))

#compiling the model
sgd = SGD(0.01)
model.compile(loss="categorical_crossentropy", optimizer=sgd,metrics=["accuracy"])
h = model.fit(X_train, y_train_en, validation_data=(X_test, y_test_en ),epochs=100, batch_size=128,
                   verbose = 1)

# plotting epoch wise training loss
figure, axis = plt.subplots(1, 2)

y1 = h.history['loss']
x1 = np.arange(0,100)
axis[0].plot(x1, y1)
axis[0].set_title('TRAINING LOSS')
axis[0].set_xlabel('EPOCHS')
axis[0].set_ylabel('CROSS ENTROPY LOSS')

y2 = h.history['val_loss']
x2 = np.arange(0,100)
axis[1].plot(x2, y2 ,color='red')
axis[1].set_title('TESTING LOSS')
axis[1].set_xlabel('EPOCHS')
axis[1].set_ylabel('CROSS ENTROPY LOSS')

plt.show()

pred = model.predict(X_test)
y_pred = np.array([np.argmax(i) for i in pred])

#testing accuracy
accuracy = accuracy_score(y_test,y_pred)
print("Accuracy : ", accuracy)

#classwise testing accuracy
cm = confusion_matrix(y_test,y_pred)
n = len(cm)
print("Class-wise accuracy")
for i in range(n):
  s = cm[i].sum()
  accuracy = cm[i][i]/s
  print("Label",i," - ",accuracy)
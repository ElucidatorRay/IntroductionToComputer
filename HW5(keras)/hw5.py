import numpy as np
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
import sys
import csv
from reader import load_fashion_mnist

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam
from keras.utils import np_utils
from keras.callbacks import EarlyStopping

num_classes = 10
img_size = 28 # mnist size = 28*28

data_dir = sys.argv[1]
output_file = sys.argv[2]


def load_data():
	# load fashion mnist data
	x_train, y_train = load_fashion_mnist(data_dir, kind='train')
	x_test, _ = load_fashion_mnist(data_dir, kind='t10k')

	# preprocess data, let pixel between 0~1
	x_train = x_train.astype('float32')/255
	y_train = np_utils.to_categorical(y_train, num_classes)

	x_test = x_test.astype('float32')/255

	return x_train, y_train, x_test

if __name__ == '__main__':
	x_train, y_train, x_test = load_data()

	# build model
	model = Sequential()
	
	# Do not modify code before this line
	# TODO: build your network.
	
	early_stopping = EarlyStopping(monitor='val_loss', patience=0, verbose=0, mode='auto')
	# input layer
	model.add(Dense(input_dim = 28*28,units = 500,activation = 'relu'))
	# hiddne layers
	model.add(Dense(units = 500,activation = 'relu'))
	model.add(Dropout(0.2))
	model.add(Dense(units = 500,activation = 'relu'))
	model.add(Dense(units = 500,activation = 'relu'))
	model.add(Dropout(0.2))
	model.add(Dense(units = 500,activation = 'relu'))
	# output layer
	model.add(Dense(units = 10,activation = 'softmax'))
	model.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])
	model.fit(x_train,y_train,batch_size = 100,epochs = 10, validation_split = 0.2, callbacks = [early_stopping])
	
	# Do not modify code after this line
	# output model
	model.summary()
	
	# output train score and test file
	score = model.evaluate(x_train, y_train)
	print('\nTrain Acc:', score[1])
	y_pred = model.predict(x_test)
	result = np.argmax(y_pred, 1)

	f = open(output_file, 'w')
	writer = csv.writer(f)
	writer.writerow(['id', 'label'])
	for i in range(x_test.shape[0]):
		writer.writerow([str(i), int(result[i])])
	f.close()

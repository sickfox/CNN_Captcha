from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.callbacks import EarlyStopping
from keras.utils import np_utils, generic_utils
import numpy as np


X_train = np.load("/var/www/html/CNN_Captcha/demo/train/x_train.npy")
Y_train = np.load("/var/www/html/CNN_Captcha/demo/train/y_train.npy")
X_test = np.load("/var/www/html/CNN_Captcha/demo/vaild/x_test.npy")
Y_test = np.load("/var/www/html/CNN_Captcha/demo/vaild/y_test.npy")

batch_size = 32
nb_classes = 144  #(10+26)*4=144
nb_epoch = 100
# input image dimensions
img_rows, img_cols = 20, 80 #圖片大小 寬*長
img_channels = 1 #gray


X_train = X_train.astype("float32")
X_train = X_train.reshape(X_train.shape[0], img_channels, img_rows, img_cols)
X_test = X_test.astype("float32")
X_test = X_test.reshape(X_test.shape[0], img_channels, img_rows, img_cols)
print(X_train.shape)
print(Y_train.shape)

model = Sequential()# 建立模型
model.add(Convolution2D(32,3,3, border_mode='same',input_shape=X_train.shape[1:]))
model.add(Activation('relu')) # 激活函數 使用relㄎu
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(64,3, 3,border_mode='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(720))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(144))
model.add(Activation('sigmoid'))

sgd = SGD(lr=1e-5, decay=0, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer='sgd')
model.fit(X_train, Y_train, batch_size= batch_size, nb_epoch= nb_epoch,validation_data = (X_test,Y_test), verbose=1)

#儲存model
model.save_weights('captcha_CNN_weights.h5')
json_string = model.to_json()
f=open('captcha_CNN_structure.json','w')
f.write(json_string)
f.close()

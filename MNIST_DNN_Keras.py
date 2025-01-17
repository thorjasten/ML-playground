# Trains a simple deep NN on the MNIST dataset.
# See https://github.com/keras-team/keras/blob/master/examples/mnist_mlp.py

from __future__ import print_function

import tensorflow as tf
import keras
from keras.datasets import mnist
# mnist = tf.keras.datasets.mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import time


# Load data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Start logging of execution time
start_time = time.time()

simple = True

if simple == True:
    """
    Up to 98.60% test accuracy after 5 epochs.
    84.5 seconds runtime on laptop
    2 seconds per epoch on a K520 GPU.
    """
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=5)
    model.evaluate(x_test, y_test)

else:
    """
    Up to 98.40% test accuracy after 20 epochs
    2 seconds per epoch on a K520 GPU.
    """
    batch_size = 128
    num_classes = 10
    epochs = 20

    # Split between train and test sets
    x_train = x_train.reshape(60000, 784)
    x_test = x_test.reshape(10000, 784)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # Convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Dense(512, activation='relu', input_shape=(784,)))
    model.add(Dropout(0.2))
    # model.add(Dense(1024, activation='relu'))
    # model.add(Dense(512, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])

    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test))
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

end_time = time.time()
print('Training time (seconds):', round((end_time - start_time), 1))

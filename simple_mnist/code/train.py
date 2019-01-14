# Copyright 2018 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import idx2numpy
import tensorflow as tf


def read_from_file(filename):
    with tf.gfile.GFile(filename, 'rb') as f:
        return idx2numpy.convert_from_file(f)


DESCRIPTION = """
This code trains a model for the MNIST dataset.
The training and test datasets are expected to be in IDX format.
You may obtain a copy of them by visiting http://yann.lecun.com/exdb/mnist/
"""

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('--training_images', help='The path to the training images file', required=True)
parser.add_argument('--training_labels', help='The path to the training labels file', required=True)
parser.add_argument('--test_images', help='The path to the test images file')
parser.add_argument('--test_labels', help='The path to the test labels file')
parser.add_argument('--model', help='The full path and the name of the model', required=True)
parser.add_argument('--batch', help='The batch size', default=32, type=int)
parser.add_argument('--epochs', help='Number of epochs', default=5, type=int)
arguments = parser.parse_args()

print('Preparing the data...')
training_images = read_from_file(arguments.training_images)
training_images = training_images.reshape(training_images.shape[0], 28, 28, 1).astype('float32') / 255.0
training_labels = read_from_file(arguments.training_labels)
training_labels = tf.keras.utils.to_categorical(training_labels)
if arguments.test_images is not None and arguments.test_labels is not None:
    test_images = read_from_file(arguments.test_images)
    test_labels = read_from_file(arguments.test_labels)
    test_images = test_images.reshape(test_images.shape[0], 28, 28, 1).astype('float32') / 255.0
    test_labels = tf.keras.utils.to_categorical(test_labels)
    validation_data = (test_images, test_labels)
else:
    validation_data = None

print('Training the MNIST model...')
model = tf.keras.Sequential()
model.add(tf.keras.layers.Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(training_images,
          training_labels,
          batch_size=arguments.batch,
          epochs=arguments.epochs,
          validation_data=validation_data)

model.save('./temporary.h5')
with open('./temporary.h5', 'rb') as in_file, tf.gfile.GFile(arguments.model, 'wb') as out_file:
    out_file.write(in_file.read())
    print('Saved the model to ' + arguments.model)

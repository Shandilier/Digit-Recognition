#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 21:48:05 2018

@author: sachin1006
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
sess = tf.InteractiveSession()


mnist = input_data.read_data_sets("Data_Recognition", one_hot=True)

# start tensorflow interactiveSession

# weight initialization
def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

#Bias initialization
def bias_variable(shape):
	initial = tf.constant(0.1, shape = shape)
	return tf.Variable(initial)

# convolution
def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
# pooling
def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

##################   MODEL CREATION  #####################
    
# placeholder
def main(argv):  
    x = tf.placeholder("float", [None, 784])
    y_ = tf.placeholder("float", [None, 10])
    
    # variables
    W = tf.Variable(tf.zeros([784,10]))
    b = tf.Variable(tf.zeros([10]))
    
    y = tf.nn.softmax(tf.matmul(x,W) + b)
    
    # first convolutional layer
    w_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    
    h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
    
    # second convolutional layer
    w_conv2 = weight_variable([5, 5, 32, 64]) 
    b_conv2 = bias_variable([64])
    
    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)  #mapping of 32 features maps int 64
    h_pool2 = max_pool_2x2(h_conv2)            #Downsampling of the feature maps size
    
    # densely connected layer
    w_fc1 = weight_variable([7*7*64, 1024])
    b_fc1 = bias_variable([1024])
    
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])     #'-1' denotes that there can be any no. of rows.
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
    
    # dropout is used to prevent overfitting.This might more time to converge but time taken per epoch reduces.
    drop = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, drop)
    
    # readout layer
    w_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])
    
    y_conv = tf.matmul(h_fc1_drop, w_fc2) + b_fc2
    
    #This function encodes alue (y) by using one-hot encoder as well as sums the rowwise losses.
    cross_entropy=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y_conv))
    
   # cross_entropy=tf.losses.sparse_softmax_cross_entropy(labels=y_,logits=y_conv)
   
   #AdamOptimizer is used as an algorithm to optimize the solution
    train_step=tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) 
    
    correct_prediction=tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
    accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32) )
        
        
    
       # tf.global_variables_initializer.run()
    sess.run(tf.global_variables_initializer())
    for i in range(20000):
        batch=mnist.train.next_batch(100)
        if(i%500==0):    #Check your prediction results after every 500 iterations.
            train_accuracy=accuracy.eval(feed_dict={x:batch[0],y_:batch[1], drop:1.0})
            print ('step {} has accuracy {}'.format(i,train_accuracy))
        sess.run(train_step,feed_dict={x:batch[0],y_:batch[1],drop:0.4})
                
        
    
    print("test accuracy %g" % accuracy.eval(feed_dict={x:mnist.test.images, y_:mnist.test.labels, drop:1.0}))    
        
    #This model attains an accuracy of 99.4% to determine which class the image belongs to(0-9)
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--data_dir',
      type=str,
      default='/tmp/tensorflow/mnist/input_data',
      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
# -*- coding: utf-8 -*-
"""RNN_SINE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hNQ_ZW4IADTsRzBtpFGcTVOpUU9HHtrD

# Recurrent Neural Network 
## Julie Hartley
### September 13, 2019
"""

# For matrices and calculations
import numpy as np
# For machine learning (backend for keras)
import tensorflow as tf
# User-friendly machine learning library
# Front end for TensorFlow
import keras
# Different methods from Keras needed to create an RNN
from keras.layers import Input
from keras.models import Model
from keras.layers.core import Dense, Activation 

from keras.layers.recurrent import SimpleRNN

# The x=values of the training data
X_train = np.arange(0, 10, 0.01)
# The value of sin(x) at those points, converted to a list
y_train = np.load('H.npy')[0:10000]

# FORMAT_DATA
def format_data(data, length_of_sequence = 2):  
    """
        Inputs:
            data(a numpy array): the data that will be the inputs to the recurrent neural
                network
            length_of_sequence (an int): the number of elements in one iteration of the
                sequence patter.  For a function approximator use length_of_sequence = 2.
        Returns:
            rnn_input (a 3D numpy array): the input data for the recurrent neural network.  Its
                dimensions are length of data - length of sequence, length of sequence, 
                dimnsion of data
            rnn_output (a numpy array): the training data for the neural network
        Formats data to be used in a recurrent neural network.
    """

    X, Y = [], []
    for i in range(len(data)-length_of_sequence):
        # Get the next length_of_sequence elements
        a = data[i:i+length_of_sequence]
        # Get the element that immediately follows that
        b = data[i+length_of_sequence]
        # Reshape so that each data point is contained in its own array
        #a = np.reshape (a, (len(a), 1))
        X.append(a)
        Y.append(b)
    rnn_input = np.array(X)
    rnn_output = np.array(Y)

    return rnn_input, rnn_output

# Generate the training data for the RNN
rnn_input, rnn_training = format_data(y_train, 2)
print()

def rnn(length_of_sequences, batch_size = None, stateful = False):
    in_out_neurons = 36
    hidden_neurons = 100
    inp = Input(batch_shape=(batch_size, 
                length_of_sequences, 
                in_out_neurons))  

    rnn = SimpleRNN(hidden_neurons, 
                    return_sequences=False,
                    stateful = stateful,
                    name="RNN")(inp)

    dens = Dense(in_out_neurons,name="dense")(rnn)
    model = Model(inputs=[inp],outputs=[dens])
    
    model.compile(loss="mean_squared_error", optimizer="adam")

    
    return(model,(inp,rnn,dens))
## use the default values for batch_size, stateful
model, (inp,rnn,dens) = rnn(length_of_sequences = rnn_input.shape[1])
model.summary()

hist = model.fit(rnn_input, rnn_training, batch_size=600, epochs=1000, 
                 verbose=False,validation_split=0.05)

import matplotlib.pyplot as plt

for label in ["loss","val_loss"]:
    plt.plot(hist.history[label],label=label)

plt.ylabel("loss")
plt.xlabel("epoch")
plt.title("The final validation loss: {}".format(hist.history["val_loss"][-1]))
plt.legend()
plt.show()

def mse (A, B):
    return np.square(np.subtract(A, B)).mean()

def test_rnn (x1, y_test, plot_min, plot_max):
    X_test, a = format_data (y_test.copy(), 2)
    y_pred = model.predict(X_test)
    plt.figure(figsize=(19,3))
    #plt.plot([10, 10, 10], [1.5, 0, -1.5])

    #x1 = x1[0:-2]
    y_test = y_test[0:-2]

    print(np.square(np.subtract(y_test, y_pred)).mean())
    fig, ax = plt.subplots()
    mse_errors = []
    for i in range(0, len(y_pred)):
        mse_errors.append(mse(y_pred[i], y_test[i]))
        if i%1000 == 0:
            print(y_test[i])
            print('*****************************')

    print(len(x1), len(mse_errors))
    plt.plot(x1, mse_errors, 'r', linewidth=5)
    plt.xlabel('Flow Parameter')
    plt.ylabel('MSE from ODE Result')
    ax.legend()
    ax.axvspan(plot_min, plot_max, alpha=0.25, color='red')
    plt.show()
    


#print('X min: 0; X max: 10, dx: 0.001')
X_test1 = np.arange(0, 50, 0.001)
y_test1 = np.load('H.npy')
test_rnn(X_test1, y_test1, 0, 10)

#print('X min: -5; X max: 5, dx=0.001')
#X_test2 = np.arange(-5, 5, 0.001)
#y_test2 = np.sin(X_test2)
#test_rnn(X_test2, y_test2, 0, 5)

#print('X min: 5; X max: 15, dx=0.001')
#X_test3 = np.arange(5, 15, 0.001)
#y_test3 = np.sin(X_test3)
#test_rnn(X_test3, y_test3, 5, 10)

#print('X min: -20; X max: 20, dx=0.1')
#X_test4 = np.arange(-20,20, 0.1)
#y_test4 = np.sin(X_test4)
#test_rnn(X_test4, y_test4, 0, 10)

#print('X min: -100; X max: 100, dx=0.1')
#X_test5 = np.arange(-100,100, 0.1)
#y_test5 = np.sin(X_test5)
#test_rnn(X_test5, y_test5, 0, 10)


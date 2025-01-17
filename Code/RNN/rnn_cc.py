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


X_tot = np.arange(2, 42, 2)
print(X_tot)
y_tot = np.array([-0.03077640549, -0.08336233266, -0.1446729567, -0.2116753732, -0.2830637392, -0.3581341341, -0.436462435, -0.5177783846,
	-0.6019067271, -0.6887363571, -0.7782028952, -0.8702784034, -0.9649652536, -1.062292565, -1.16231451, 
	-1.265109911, -1.370782966, -1.479465113, -1.591317992, -1.70653767])

assert len(X_tot) == len(y_tot)

X_train = X_tot[0:10]
y_train = y_tot[0:10]

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
        a = np.reshape (a, (len(a), 1))
        X.append(a)
        Y.append(b)
    rnn_input = np.array(X)
    rnn_output = np.array(Y)

    return rnn_input, rnn_output

# Generate the training data for the RNN
rnn_input, rnn_training = format_data(y_train, 2)
print(rnn_input)


def rnn(length_of_sequences, batch_size = None, stateful = False):
    in_out_neurons = 1
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

def test_rnn (x1, y_test, plot_min, plot_max):
    X_test, a = format_data (y_test.copy(), 2)
    y_pred = model.predict(X_test)
    plt.figure(figsize=(19,3))
    #plt.plot([10, 10, 10], [1.5, 0, -1.5])

    x1 = x1[0:-2]
    y_test = y_test[0:-2]

    print(np.square(np.subtract(y_test, y_pred.flatten())).mean())
    fig, ax = plt.subplots()
    ax.plot(x1, y_test, label="true", linewidth=2)
    ax.plot(x1, y_pred, 'g-.',label="predicted", linewidth=2)
    ax.legend()

    ax.axvspan(plot_min, plot_max, alpha=0.25, color='red')
    plt.show()
    
    diff = y_test - y_pred.flatten()

    plt.plot(x1, diff, linewidth=4)
    plt.show()

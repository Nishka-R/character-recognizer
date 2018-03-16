import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.utils import to_categorical
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D
from keras.layers.advanced_activations import LeakyReLU 
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import yaml

def read_transform_data(train_file, test_file):
    """Read in the training and test data and reshape them for the neural network model.
    
    Args:
        train_file (str): The path of the file containing the training data.
        test_file (str): The path of the file containing the testing data.

    Returns:
        tuple: A 4-tuple of numpy arrays containing training predictors and response and testing predictors and response respectively.

    """
    logging.info('Executing function read_transform_data().')

    # reading the train and test data
    logging.info('Reading training and testing data.')
    try:
        with open(train_file,'r') as f:
            train = pd.read_csv(train_file, header = None)
    except IOError: 
        raise SystemExit("The file you are trying to read does not exist: " + train_file)

    try:
        with open(test_file,'r') as f:
            test = pd.read_csv(test_file, header = None)
    except IOError: 
        raise SystemExit("The file you are trying to read does not exist: " + test_file)

    # separate out the train data from the response variable
    logging.info('Separating out the train data from the response variable.')
    X_train = train.iloc[:, 1:]
    X_test = test.iloc[:, 1:]

    # separate out the response variable from the data
    logging.info('Separating out the response variable from the data.')
    Y_train = train[0]
    Y_test = test[0]

    # converting the pandas dataframe to numpy matrices
    logging.info('Converting the pandas dataframe to numpy matrices.')
    X_train = X_train.values
    Y_train = Y_train.values
    X_test = X_test.values
    Y_test = Y_test.values

    # reshaping the data into the format which can be passed to the neural network
    logging.info("Reshaping the data into the format which can be passed to the neural network.")
    X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
    X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)

    # converting the data type to float32
    logging.info("Converting the data type to float32.")
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    # Normalizing the predictors
    logging.info("Normalizing the predictors.")
    X_train/=255
    X_test/=255

    # Defining the number of classes in the response variable
    logging.info("Defining the number of classes in the response variable.")
    number_of_classes = 47

    # One hot encoding the response variable
    logging.info("One hot encoding the response variable.")
    Y_train = to_categorical(Y_train, number_of_classes)
    Y_test = to_categorical(Y_test, number_of_classes)

    # Returning the training and testing predictors and response. Function succesfully completed
    logging.info("Returning the training and testing predictors and response. Function read_transform_data() succesfully completed.")
    return X_train, Y_train, X_test, Y_test

def build_convnet():
    """Build a sparse convolutional neural network model.

    Steps to create a Convolutional Neural Network
    1. Add convolution layers
    2. Add activation function
    3. Add pooling layers
    4. Repeat Steps 1,2,3 for adding more hidden layers
    5. Finally, add a fully connected softmax layer giving the CNN the ability to classify the samples

    Returns:
        Keras Sequential Model: A convolutional neural network model.

    """
    logging.info('Executing function build_convnet().')

    # Defining the number of classes in the response variable
    logging.info("Defining the number of classes in the response variable.")
    number_of_classes = 47

    # Adding the first set of convolutional and pooling layers with ReLu activation
    logging.info("Adding the first set of convolutional and pooling layers with ReLu activation.")
    model = Sequential()
    model.add(Conv2D(64, (3, 3), input_shape=(28,28,1)))
    model.add(BatchNormalization(axis=-1))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(BatchNormalization(axis=-1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    # Adding the second set of convolutional and pooling layers with ReLu activation
    logging.info("Adding the second set of convolutional and pooling layers with ReLu activation.")
    model.add(Conv2D(128,(3, 3)))
    model.add(BatchNormalization(axis=-1))
    model.add(Activation('relu'))
    model.add(Conv2D(128, (3, 3)))
    model.add(BatchNormalization(axis=-1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())

    # Adding fully connected layers with softmax activation and 20% dropout
    logging.info("Adding fully connected layers with softmax activation and 0.20 dropout.")
    model.add(Dense(1024))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(number_of_classes))
    model.add(Activation('softmax'))

    # Compiling the model with categorical crossentropy loss function to handle multiple classes
    logging.info("Compiling the model with categorical crossentropy loss function to handle multiple classes.")
    model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

    # Returning the completed model
    logging.info("Returning the completed model. Function build_convnet() executed successfully.")
    return model

def train_test(model, X_train, Y_train, X_test, Y_test, model_name):
    """Fit the convolutional neural network model on the training data, evaluate on the test data, and save it to disk.
    
    Args:
        model (Keras model): The path of the file containing the training data.
        X_train (ndarray): A numpy array with shape (n,28,28,1) containing the predictors for n images in the train data.  
        Y_train (ndarray): A numpy array with shape (n,) containing the response classes for n images in the train data.
        X_test (ndarray): A numpy array with shape (n,28,28,1) containing the predictors for n images in the test data.
        Y_test (ndarray): A numpy array with shape (n,) containing the response classes for n images in the train data.
        model_name (str): The filename to save the keras model to.

    """ 
    logging.info('Executing function train_test().')

    # Setting the batch size and number of epochs
    logging.info("Setting the batch size and number of epochs.")
    batch_size=256
    epochs=10

    # Training the model on the train data
    logging.info("Training the model on the train data.")
    model.fit(X_train, Y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(X_test, Y_test))

    # Evaluating the model on the test data
    logging.info("Evaluating the model on the test data.")
    score = model.evaluate(X_test, Y_test, verbose=1)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    # Saving the model to disk
    logging.info("Saving the model to disk.")
    model.save("develop/models/" + model_name)
    logging.info("Function train_test() executed succesfully.")                                                         

def main(metadata):
    """Read the train and test data, build, train, evaluate and save the conv net.
    
    Args:
        metadata (file object): The file object of the metadata file.

    """
    logging.info('Executing function main().')

    # train and test file locations
    train_file = "develop/data/" + metadata['train_file']
    test_file = "develop/data/" + metadata['test_file']

    # defining the model name
    model_name = metadata['model_name']

    # creating the training and testing set
    X_train, Y_train, X_test, Y_test = read_transform_data(train_file, test_file)

    # building the model
    model = build_convnet()

    # training, evaluating, and saving the model
    train_test(model, X_train, Y_train, X_test, Y_test, model_name)
    logging.info("Function main() executed successfully.")

def read_metadata(metadata_file_path):
    """Read the YAML file containing metadata
    
    Args:
        metadata_file_path (str): The path of the file containing the training data.

    Returns:
        File Object: File object of the YAML metadata file.
        
    """
    logging.info('Executing function read_metadata().')

    # reading and loading metadata from yaml file    
    try:
        with open(metadata_file_path,'r') as metadata_file:            
            metadata = yaml.load(metadata_file)
    except IOError: 
        raise SystemExit("The file you are trying to read does not exist: " + metadata_file_path)

    # returning the metadata dictionary
    logging.info("Function read_metadata() executed successfully.")
    return metadata

if __name__ == '__main__':
    # setting up the logging file and formats
    log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
    date_fmt = '%m/%d/%Y %I:%M:%S %p'
    logging.basicConfig(filename='develop/logs/model_balanced_dense.log', filemode='w',  level=logging.DEBUG, format = log_fmt, datefmt = date_fmt)
    
    # defining the metadata file path
    metadata_file_path = "develop/metadata.yaml"

    # reading the metadata file
    metadata = read_metadata(metadata_file_path)

    # calling the main function
    main(metadata)
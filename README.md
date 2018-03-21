# Character Recognizer

Character recognition project for the course MSiA423: Analytics Value Chain.

- #### Developer: Rishabh Joshi 

- Product Owner: Lauren Gardiner

- Quality Assurance: Vincent Wang

## Project Charter

Predict the character drawn by the user on the web app by using a neural network model based on the grayscale pixel values of the image to assist in building a handwriting input keyboard system that can be employed on different smartphones.

### Vision 

Assist in building a handwriting input keyboard system that can be employed on different smartphones.

### Mission 

Predict the character drawn by the user on the web app by using a neural network model based on the grayscale pixel values of the image.

### Success criteria 

Accuracy of classification for the neural network on a pre-determined test set of grayscale character images.

## Getting Started

### Dependencies

Dependencies are listed in the [develop/requirements.txt](develop/requirements.txt)

### Documentation

This project was documented using Sphinx and the documentation files can be found in the [develop\docs\_build\html](develop\docs\_build\html) folder.

### Repository Structure

The two main folders in this repository are [app](app) and [develop](develop) which contains the code to deploy the app and the code for model development respectively.

### Steps to Deploy Application

1. Install python 3.6
```
    sudo yum install python36
```
2. Create a virtual environment.
```
    virtualenv -p python3 turnover
    source turnover/bin/activate
```
3. Install Git.
```
    sudo yum install git
```
4. Clone the repository
```
    git clone https://github.com/rishabh-joshi/character-recognizer.git
```
5. Change directory
```
    cd character-recognizer
```
6. Create a file "config" in the app folder which stores database credentials as described below.
```
    SQLALCHEMY_DATABASE_URI = 'postgresql://<db_user>:<db_password>@<endpoint>/<db_url>'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
```
7. Export environment variables from the config file.
```
    export APP_SETTINGS="config"
```
8. Download the following csv data files from Kaggle and extract them into the [develop/data](develop/data) folder.
    - [EMNIST Balanced Train Data](https://www.kaggle.com/crawford/emnist/downloads/emnist-balanced-train.csv/3)
    - [EMNIST Balanced Test Data](https://www.kaggle.com/crawford/emnist/downloads/emnist-balanced-test.csv/3)
    - [EMNIST By Class Train Data](https://www.kaggle.com/crawford/emnist/downloads/emnist-byclass-train.csv/3)
    - [EMNIST By Class Test Data](https://www.kaggle.com/crawford/emnist/downloads/emnist-byclass-test.csv/3)
9. Run the unit tests to ensure that there are no bugs in the model development and deployment code.
```
cd develop/src/tests
pytest
cd ../../..
```
10. There are four convolutional neural network models to choose from for the prediction of characters. These are called `sparse_cnn_balanced`, `dense_cnn_balanced`, `sparse_cnn_byclass`, and `dense_cnn_byclass`. Because these models take a long time to train, they have been trained and provided as h5 files in the [develop/models](develop/models) directory. They can be read in through Keras.
11. [OPTIONAL STEP] The best performing model from the above four models is `sparse_cnn_byclass` which is chosen by default. If the models are to be retrained, modify the [develop/metadata.yaml](develop/metadata.yaml) with the name of the model to be retrained as follows. Replace the name of the model and the corresponding data file in the YAML file while preserving the extension of the files.
```
train_file : emnist-byclass-train.csv
test_file : emnist-byclass-test.csv
model_name : sparse_cnn_byclass.h5
```
12. [OPTIONAL STEP] For every model that needs retraining, run the following make command by appropriately changing the model name.
```
make sparse_cnn_byclass
```
13. Finally, once the models have been fitted, specify the model that should be used for prediction purposes in the [develop/metadata.yaml](develop/metadata.yaml) file by changing the name of the h5 file in which the model is saved with the model you want to use.
```
model_name : sparse_cnn_byclass.h5
```
14. We are now in a position to deploy the app.
```
python36 app/application.py
```
15. Check out the app by visiting the IP address that appeared on the consol after the app has been successfully deployed.






from model_balanced_dense import *

# reading the metadata file
metadata_file_path = "../../metadata.yaml"
metadata = yaml.load(open(metadata_file_path))

# train and test file locations
train_file = "../../data/" + metadata['train_file']
test_file = "../../data/" + metadata['test_file']

# defining the number of classes
number_of_classes = 47

def test_build_convnet_model_type():
    # model should be a keras Sequrntial model
    model = build_convnet()
    assert isinstance(model, keras.models.Sequential)

def test_build_convnet_input_dim():
    # checking the input dimension of the model
    model = build_convnet()
    assert model.input_shape == (None, 28, 28, 1)

def test_build_convnet_output_dim():
    # checking the output dimension of the model
    model = build_convnet()
    assert model.output_shape == (None, number_of_classes)

def test_build_convnet_metrics():
    # checking the the model testing metrics
    model = build_convnet()
    assert ('accuracy' in model.metrics and 'loss' in  model.metrics_names and 'acc' in model.metrics_names)

def test_build_convnet_built():
    # the model should be compiled and built
    model = build_convnet()
    assert model.built

def test_read_transform_data_IOError():
    # checking to see if the train and test file exist or not
    with pytest.raises(SystemExit):
        read_transform_data(train_file, test_file)

def test_read_transform_data_train_X_dim():
    # checking the dimensions of the training predictors
    X_train, Y_train, X_test, Y_test = read_transform_data(train_file, test_file)
    assert X_train.shape[1:] == (28, 28, 1)

def test_read_transform_data_test_X_dim():
    # checking the dimensions of the test predictors
    X_train, Y_train, X_test, Y_test = read_transform_data(train_file, test_file)
    assert X_test.shape[1:] == (28, 28, 1)

def test_read_transform_data_train_Y_dim():
    # checking the dimensions of the training response
    X_train, Y_train, X_test, Y_test = read_transform_data(train_file, test_file)
    assert Y_train.shape[1] == number_of_classes

def test_read_transform_data_test_Y_dim():
    # checking the dimensions of the test response
    X_train, Y_train, X_test, Y_test = read_transform_data(train_file, test_file)
    assert Y_test.shape[1] == number_of_classes

def test_main_IOError():
    # checking to see if the train and test file exist or not
    with pytest.raises(SystemExit):
        main(metadata_file_path)
from os import path, listdir
from keras.models import Sequential
from keras.layers import Conv2D, Dropout, Dense, GlobalMaxPooling2D

def build_network():
    in_shape = (None, None, 3)
    classes = 2

    model = Sequential()

    model.add(Conv2D(16, 3, activation='relu', input_shape=in_shape))
    model.add(Conv2D(32, 3, activation='relu'))
    model.add(Conv2D(48, 3, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, 3, activation='relu'))
    model.add(Dropout(0.25))

    model.add(GlobalMaxPooling2D())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    return model

def check_directories(dir):
    if not path.exists(dir) or listdir(dir) == []:
        return False
    else:
        return True

def train():

    train_data_dir = "data\\training"
    validation_data_dir = "data\\validation"

    if not check_directories(train_data_dir):
        print("Unable to run training - no training data provided.\nAborting training.\n")
        return
    
    if not check_directories(validation_data_dir):
        print("Unable to run training - no validation data provided.\nAborting training.\n")
        return

    print("\nAttempting to build the network...")

    model = build_network()
    model.summary()


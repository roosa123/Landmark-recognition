from os import path, listdir
from keras.models import Sequential
from keras.layers import Conv2D, Dropout, Dense, GlobalMaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

def check_directories(dir):
    if not path.exists(dir) or listdir(dir) == []:
        return False
    else:
        return True

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

    model.summary()

    return model

def preprocess_data():
    train_data = ImageDataGenerator(
                    rotation_range=45,
                    horizontal_flip=True,
                    height_shift_range=0.1,
                    width_shift_range=0.1
                ).flow_from_directory(
                    'data\\training',
                    target_size=(200, 200),
                    batch_size=32
                )
    validation_data = ImageDataGenerator().flow_from_directory(
                    'data\\validation',
                    target_size=(200, 200),
                )

    return (train_data, validation_data)

def train(model: Sequential, data: tuple):
    (train_data, val_data) = data

    checkpoint = ModelCheckpoint('best_model', monitor='val_loss', save_best_only=True)

    model.fit_generator(
        train_data,
        steps_per_epoch=64,
        epochs=1000,
        callbacks=[checkpoint],
        validation_data=val_data,
        validation_steps=2
    )

def run_training(model: Sequential):

    train_data_dir = "data\\training"
    validation_data_dir = "data\\validation"

    if not check_directories(train_data_dir):
        print("Unable to run training - no training data provided.\nAborting training.\n")
        return
    
    if not check_directories(validation_data_dir):
        print("Unable to run training - no validation data provided.\nAborting training.\n")
        return

    print("\nAttempting to train the network...")

    futer_do_sieci = preprocess_data()

    train(model, futer_do_sieci)

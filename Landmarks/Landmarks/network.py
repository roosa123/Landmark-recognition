import numpy as np
from os import path, listdir
from keras.models import Model
from keras.layers import Conv2D, Dropout, Dense, Flatten, Activation, MaxPooling2D, Input
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.utils import plot_model
from utilities import check_directories
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def normalize_image(n):
    return np.divide(np.subtract(np.array(n), 127.5), 127.5)

def build_network():
    network_input = Input(shape=(128, 128, 3))
    in_shape = (128, 128, 3)
    classes = 2

    # model = Sequential()

    # model.add(Conv2D(32, (3, 3), padding='same', input_shape=in_shape))
    # model.add(Activation('relu'))
    # model.add(Conv2D(32, (3, 3)))
    # model.add(Activation('relu'))
    # model.add(MaxPooling2D(pool_size=(2,2)))
    # model.add(Dropout(0.25))

    # model.add(Conv2D(64, (3, 3), padding='same'))
    # model.add(Activation('relu'))
    # model.add(Conv2D(64, (3, 3)))
    # model.add(Activation('relu'))
    # model.add(MaxPooling2D(pool_size=(2,2)))
    # model.add(Dropout(0.25))

    # model.add(Flatten())

    # model.add(Dense(512, activation='relu'))
    # model.add(Dropout(0.5))
    # model.add(Dense(classes))
    # model.add(Activation('softmax'))

    # convolutional layers
    conv_1 = Conv2D(32, 3, padding='same', activation='relu', input_shape=in_shape)(network_input)
    conv_2 = Conv2D(48, 3, activation='relu')(conv_1)
    conv_3 = Conv2D(64, 3, activation='relu')(conv_2)
    max_pool_1 = MaxPooling2D(pool_size=(2,2))(conv_3)
    dropout_1 = Dropout(0.25)(max_pool_1)
    conv_4 = Conv2D(32, 3, activation='relu', padding='same')(dropout_1)
    conv_5 = Conv2D(48, 3, activation='relu')(conv_4)
    conv_6 = Conv2D(64, 3, activation='relu')(conv_5)
    max_pool_2 = MaxPooling2D(pool_size=(2,2))(conv_6)
    dropout_2 = Dropout(0.25)(max_pool_2)
    conv_7 = Conv2D(32, 3, activation='relu', padding='same')(dropout_2)
    conv_8 = Conv2D(48, 3, activation='relu')(conv_7)
    conv_9 = Conv2D(64, 3, activation='relu')(conv_8)
    max_pool_3 = MaxPooling2D(pool_size=(2,2))(conv_9)
    dropout_3 = Dropout(0.25)(max_pool_3)

    # classifier 1 - classifies images
    flatten_1_1 = Flatten()(dropout_3)
    dense_1_1 = Dense(128, activation='relu')(flatten_1_1)
    dropout_3_1 = Dropout(0.25)(dense_1_1)
    out_1 = Dense(classes, activation='softmax')(dropout_3_1)

    # classifier 2 - locates objects
    # flatten_1_2 = Flatten()(dropout_2)
    # dense_1_2 = Dense(512, activation='relu')(flatten_1_2)
    # dropout_3_2 = Dropout(0.25)(dense_1_2)
    # out_2 = Dense(classes, activation='softmax')(dropout_3_2)

    # model = Model(inputs=network_input, outputs=[out_1, out_2])

    model = Model(inputs=network_input, outputs=out_1)

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    # model summaries - in the form of the jpg image with schematics and a printed table

    try:
        plot_model(model, to_file="model.jpg", show_layer_names=True, show_shapes=True)
    except:
        print("Unable to plot the model architecture - have you got installed Graphviz?\nSkipping plotting.\n")
    
    model.summary()

    return model

def preprocess_data():
    train_data = ImageDataGenerator(
                    rotation_range=45,
                    horizontal_flip=True,
                    height_shift_range=0.1,
                    width_shift_range=0.1,
                    preprocessing_function=normalize_image
                ).flow_from_directory(
                    'data\\training',
                    target_size=(128, 128),
                    batch_size=32
                )
    validation_data = ImageDataGenerator(
                    preprocessing_function=normalize_image
                ).flow_from_directory(
                    'data\\validation',
                    target_size=(128, 128),
                )

    return (train_data, validation_data)

def train(model: Model, data: tuple):
    (train_data, val_data) = data

    checkpoint = ModelCheckpoint('best_model', monitor='val_loss', save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', min_delta=0.005, patience=5)

    model.fit_generator(
        train_data,
        steps_per_epoch=64,
        epochs=500,
        callbacks=[checkpoint, early_stopping],
        validation_data=val_data,
        validation_steps=2
    )

def run_training():
    train_data_dir = "data\\training"
    validation_data_dir = "data\\validation"

    if not check_directories(train_data_dir):
        print("Unable to run training - no train data found.\nTraining aborted.\n")
        return
    
    if not check_directories(validation_data_dir):
        print("Unable to run training - no validation data found.\nTraining aborted.\n")
        return

    print("\nAttempting to train the network...")

    model = build_network()
    futer_do_sieci = preprocess_data()
    train(model, futer_do_sieci)

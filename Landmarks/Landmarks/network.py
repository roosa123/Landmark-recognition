from os import path, listdir
from keras.models import Sequential, Model
from keras.layers import Conv2D, Dropout, Dense, Flatten, Activation, MaxPooling2D, Input
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from keras.utils import plot_model

def check_directories(dir):
    if not path.exists(dir) or listdir(dir) == []:
        return False
    else:
        return True

def build_network():
    network_input = Input(shape=(200, 200, 3))
    in_shape = (200, 200, 3)
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
    conv_1 = Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=in_shape)(network_input)
    conv_2 = Conv2D(32, (3, 3), activation='relu')(conv_1)
    max_pool_1 = MaxPooling2D(pool_size=(2,2))(conv_2)
    dropout_1 = Dropout(0.25)(max_pool_1)
    conv_3 = Conv2D(64, (3, 3), activation='relu', padding='same')(dropout_1)
    conv_4 = Conv2D(64, (3, 3), activation='relu')(conv_3)
    max_pool_2 = MaxPooling2D(pool_size=(2,2))(conv_4)
    dropout_2 = Dropout(0.25)(max_pool_2)

    # classifier 1 - classifies images
    flatten_1 = Flatten()(dropout_2)
    dense_1 = Dense(512, activation='relu')(flatten_1)
    dropout_3 = Dropout(0.25)(dense_1)
    out_1 = Dense(classes, activation='softmax')(dropout_3)

    # classifier 2 - locates objects
    flatten_2 = Flatten()(dropout_2)
    dense_1_2 = Dense(512, activation='relu')(flatten_2)
    dropout_3_2 = Dropout(0.25)(dense_1_2)
    out_2 = Dense(classes, activation='softmax')(dropout_3_2)

    model = Model(inputs=network_input, outputs=[out_1, out_2])

    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    # model summaries - in the form of the jpg image with schematics and a printed table

    plot_model(model, to_file="model.jpg", show_layer_names=True, show_shapes=True)
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
        epochs=500,
        callbacks=[checkpoint],
        validation_data=val_data,
        validation_steps=2
    )

    model.save("cur_model")

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

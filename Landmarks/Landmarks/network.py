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

def train():
    print("\nBuiliding the network...")
    model = build_network()
    model.summary()


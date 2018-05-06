import glob
import matplotlib.pyplot as plt
import matplotlib.image as plt_img
import numpy as np
from os import path
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from network import build_network
from os import listdir

def show(test_img, prediction, img_no):
    classes = ["Florence", "Museu Nacional d'Art de Catalunya"]

    img = plt_img.imread(path.join("data\\testing", test_img))

    plt.imshow(img)     # tu trzeba bedzie pozmieniac
    class_index = np.argmax(prediction)
    plt.title(classes[img_no] + ": " + str(prediction[class_index]), fontsize=10)
    plt.axis('off')

    plt.show()

def classify(model: Sequential):
    test_data_generator = ImageDataGenerator()
    test_data = test_data_generator.flow_from_directory(
                    'data\\testing',
                    target_size=(200, 200),
                    batch_size=32
                    )

    if model is None:
        model = build_network()

    model.load_weights('best_model')
    output = model.predict_generator(test_data)

    print(len(output))
    print(len(test_data.filenames))

    for i in range(len(output)):
        show(test_data.filenames[i], output[i], i)

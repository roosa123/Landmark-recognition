import glob
import matplotlib.pyplot as plt
import matplotlib.image as plt_img
import numpy as np
from os import path
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model, load_model
from network import build_network
from os import listdir
from network import check_directories

def show(test_img, prediction, img_no):
    classes = ["Florence", "Museu Nacional d'Art de Catalunya"]

    img = plt_img.imread(path.join("data\\testing", test_img))

    plt.imshow(img)
    class_index = np.argmax(prediction)
    plt.title(classes[class_index] + ": " + str(prediction[class_index]), fontsize=10)
    plt.axis('off')

    plt.show()

def classify(model: Model):
    test_data_generator = ImageDataGenerator()
    test_data = test_data_generator.flow_from_directory(
                    'data\\testing',
                    target_size=(200, 200),
                    batch_size=32
                    )

    if model is None:
        load_model("cur_model")

    model.load_weights('best_model')
    output = model.predict_generator(test_data)

    print(len(output))
    print(len(test_data.filenames))

    for i in range(len(output)):
        print(len(output[i]))
        print(output[i])
        show(test_data.filenames[i], output[i], i)

def run_classification(model: Model):
    test_dir = "data\\testing"

    if not check_directories(test_dir):
        print("Unable to run classification - no testing data found.\nAborting classsification.\n")
        return

    classify(model)

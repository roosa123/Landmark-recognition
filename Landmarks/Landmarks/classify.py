import matplotlib.pyplot as plt
import matplotlib.image as plt_img
import numpy as np
from matplotlib import rcParams
from os import path, listdir
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model, load_model
from network import build_network, normalize_image
from utilities import check_directories

def show(test_img, prediction, img_no):
    classes = ["Ponte di Rialto", "Museu Nacional d'Art de Catalunya"]

    img = plt_img.imread(path.join("data\\testing", test_img))

    plt.imshow(img)
    class_index = np.argmax(prediction)
    plt.title(classes[class_index] + ": " + str(prediction[class_index]), fontsize=10)
    plt.axis('off')

    # plt.show()
    plt.pause(.6)
    plt.draw()

def classify():
    test_data = ImageDataGenerator(
                    preprocessing_function=normalize_image
                ).flow_from_directory(
                    'data\\testing',
                    target_size=(128, 128),
                    batch_size=32
                )

    model = load_model("best_model_loss")

    output = model.predict_generator(test_data)

    rcParams['toolbar'] = 'None'

    for i in range(len(output)):
        show(test_data.filenames[i], output[i], i)

    plt.close()

def run_classification():
    test_dir = "data\\testing"

    if not check_directories(test_dir):
        print("Unable to run classification - no test data found.\nClasssification aborted.\n")
        return

    if not path.exists("best_model"):
        print("Unable to run classification - no model found.\nClasssification aborted.\n")
        return

    classify()

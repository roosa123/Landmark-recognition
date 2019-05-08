import matplotlib.pyplot as plt
import matplotlib.image as plt_img
import numpy as np
import seaborn as sns
from matplotlib import rcParams
from os import path, listdir
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model, load_model
from network import build_network, normalize_image
from utilities import check_directories
from sklearn.metrics import confusion_matrix
from pandas import DataFrame

def show(test_img, prediction, img_no):
    classes = ["Charles Bridge", "Pantheon", "Ponte di Rialto", "Petronas Towers", "Florence", "Museu Nacional d'Art de Catalunya", "Palazzo Pubblico", "Alhambra"]

    img = plt_img.imread(path.join("data\\testing", test_img))

    plt.imshow(img)
    class_index = np.argmax(prediction)
    plt.title(classes[class_index] + ": " + str(int(100* prediction[class_index])) + '%', fontsize=10)
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
                    batch_size=8,
                    shuffle=False
                )

    model = load_model("best_model")

    output = model.predict_generator(test_data, steps=len(test_data), verbose=1)

    rcParams['toolbar'] = 'None'

    predicted_classes = np.argmax(output, axis=1)
    true_classes = test_data.classes

    labels = ["Charles Bridge", "Pantheon", "Ponte di Rialto", "Petronas Towers", "Florence", "Museu Nacional d'Art de Catalunya", "Palazzo Pubblico", "Alhambra"]

    pred = []
    true = []

    for i in range(len(predicted_classes)):
        pred.append(labels[predicted_classes[i]])
        true.append(labels[true_classes[i]])

    conf_matrix = confusion_matrix(true, pred, labels)

    width, height = conf_matrix.shape
    annots = np.empty_like(conf_matrix).astype(str)

    sums = np.sum(conf_matrix, axis=1, keepdims=True)
    percentage = conf_matrix / sums * 100

    for i in range(width):
        for j in range(height):
            if i == j:#'%.1f%%\n%d/%d' % (p, c, s)
                annots[i, j] = ("%.1f%%\n%d/%d" % (percentage[i, j], conf_matrix[i, j], sums[i]))
            else:
                annots[i, j] = ("%.1f%%\n%d" % (percentage[i, j], conf_matrix[i, j]))


    conf_matrix = DataFrame(conf_matrix)

    fig, ax = plt.subplots(figsize=(30, 15))
    plt.tight_layout(pad=2.5, h_pad=2.5, w_pad=2.5, rect=[0.2, 0.3, 1, 1])

    sns.set(font_scale=1.4)
    sns.heatmap(conf_matrix, annot=annots, fmt='', ax=ax)

    ax.set_xlabel("Predicted", fontsize=30)
    ax.set_ylabel("Actual", fontsize=30)

    x = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]

    ax.set_xticks(x)
    ax.set_yticks(x)
    ax.set_xticklabels(labels, rotation=45, fontsize=15)
    ax.set_yticklabels(labels, rotation=45, fontsize=15)

    plt.savefig('confusion_matrix.jpg')

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

# classify()
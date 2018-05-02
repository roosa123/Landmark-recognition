import glob
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing.image import img_to_array, array_to_img, load_img
from keras.models import Sequential

def show(test_data, prediction, img_no):
    classes = ["Florence", "Museu Nacional d'Art de Catalunya"]

    plt.imshow(array_to_img(test_data[img_no]))
    class_index = np.argmax(prediction)
    plt.title(classes[img_no] + ": " + prediction[class_index], fontsize=40)
    plt.axis('off')

def classify(model: Sequential):
    cos = glob.glob("data/test/*")
    test_data = [
        img_to_array(load_img(filename))
        for filename in cos
    ]
    
    model.load_weights('best_model')
    output = model.predict(test_data)

    for i in range(len(output)):
        show(test_data[i], output[i], i)

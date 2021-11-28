import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('Movierecommendation/movie_model_1.h5')

def recommend(data):
    array1 = np.zeros((1,1))
    array2 = np.zeros((1,1))
    array1[0][0]=data
    array2[0][0] = 0
    list_of_predictions = []
    while (array2[0][0]<2000):
        y_testing_model = model.predict([array1,array2])
        list_of_predictions.append((array2[0][0], float(y_testing_model)))
        array2[0][0] +=1
        #print(array2[0][0])

    sorted_list = sorted(list_of_predictions, key = lambda x: float(x[1]), reverse = True)
    
    return sorted_list[:10]
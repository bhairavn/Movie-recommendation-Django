import pickle
def returnlabel(text):
    filename = 'Movierecommendation/nlpmodel'
    model1 = pickle.load(open(filename, 'rb'))
    if model1.predict([text])[0] == 1:
    	return(int(1))
    else:
    	return(int(0))